 -- This function loads data from a CSV file into a specified table in the database.
CREATE OR REPLACE FUNCTION load_table_from_csv(schema_name TEXT, table_name TEXT, csv_file_path TEXT)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('COPY %I.%I FROM %L WITH (FORMAT CSV, HEADER, DELIMITER '','')',
                   schema_name, table_name, csv_file_path);
END;
$$;

-- Create a view named monthly_active_users_of_city_name
-- to aggregate data about monthly active users based on their orders in in the specified city
CREATE OR REPLACE FUNCTION monthly_active_users_view_by_city(city_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('
        CREATE OR REPLACE VIEW monthly_active_users_of_%s AS
        SELECT
            c.customer_number,
            c.city,
            TO_CHAR(DATE_TRUNC(''month'', o.shipped_date), ''YYYY-Month'') AS active_month,
            COUNT(DISTINCT o.order_number) AS orders_count
        FROM
            customers c
        JOIN
            orders o ON c.customer_number = o.customer_number
        WHERE
            o.status = ''Shipped''
            AND c.city = ''%s''
        GROUP BY
            c.customer_number, c.city, active_month
        HAVING
            COUNT(DISTINCT o.order_number) >= 1;
    ', city_name, city_name);

END
$$ LANGUAGE plpgsql;


-- The function return the top 10 customers who have made the most purchases in the first half of the year.
DROP FUNCTION IF EXISTS get_top_customers_with_most_purchases_first_half_year(integer);
CREATE FUNCTION get_top_customers_with_most_purchases_first_half_year(year INT)
RETURNS TABLE(
    customer_number BIGINT,
    contact_firstname VARCHAR,
    contact_lastname VARCHAR,
    total_orders BIGINT
    ) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.customer_number,
        c.contact_firstname,
        c.contact_lastname,
        COUNT(o.order_number) AS total_orders
    FROM
        customers c
    JOIN
        orders o ON c.customer_number = o.customer_number
    WHERE
        o.shipped_date BETWEEN make_date(year, 1, 1) AND make_date(year, 6, 30)
    GROUP BY
        c.customer_number, c.contact_firstname, c.contact_lastname
    ORDER BY
        total_orders DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

/*
Function to calculate the monthly profit by city in the given year.
Description:
This function calculates the total profit from all products for each city every month in the given year,
considering any discounts applied to those products.
The profit is calculated as the difference between the selling price and the buy price,
adjusted for any discounts applied. The results are grouped by city and month and total profit.
*/
DROP FUNCTION IF EXISTS get_monthly_profit_by_city(INT);
CREATE FUNCTION get_monthly_profit_by_city(year INT)
RETURNS TABLE(city VARCHAR, Month TEXT, total_profit NUMERIC(10,2)) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.city,
        TO_CHAR(DATE_TRUNC('month', o.shipped_date),'Month') AS Month,
        SUM(
            (od.price_each - COALESCE(ob.buy_price, 0) -
            CASE
                WHEN o.order_date BETWEEN pd.date_created AND pd.valid_until THEN
                    CASE
                        WHEN pd.discount_unit = 'P' THEN (pd.discount_value / 100.0) * od.price_each
                        WHEN pd.discount_unit = 'A' THEN pd.discount_value
                        ELSE 0
                    END
                ELSE 0
            END) * od.quantity_ordered
        )::numeric(10, 2) AS total_profit
    FROM
        customers c
    JOIN
        orders o ON c.customer_number = o.customer_number
    JOIN
        order_details od ON o.order_number = od.order_number
    LEFT JOIN
        production.products_discount pd ON od.product_code = pd.product_code
    LEFT JOIN
        office_buys ob ON od.product_code = ob.product_code
    WHERE
        o.shipped_date BETWEEN make_date(year, 1, 1) AND make_date(year, 12, 31)
      AND pd.in_active = TRUE
    GROUP BY
        c.city, DATE_TRUNC('month', o.shipped_date)
    ORDER BY
        c.city, DATE_TRUNC('month', o.shipped_date), "total_profit" DESC;
END;
$$ LANGUAGE plpgsql;


--Function to retrieve a report of product changes within a specified time frame.
DROP FUNCTION IF EXISTS production.get_product_changes_report(TIMESTAMP, TIMESTAMP);
CREATE FUNCTION production.get_product_changes_report(start_date TIMESTAMP, end_date TIMESTAMP)
RETURNS TABLE (
    the_product_code VARCHAR(15),
    the_product_name VARCHAR(70),
    the_change_count BIGINT
    ) AS $$
BEGIN
    RETURN QUERY
    WITH all_changes AS (
        SELECT product_code, operation_timestamp AS change_timestamp
        FROM logs.product_changes_log
        WHERE operation_timestamp BETWEEN start_date AND end_date
        UNION ALL
        SELECT product_code, operation_timestamp
        FROM logs.product_pricing_changes_log
        WHERE operation_timestamp BETWEEN start_date AND end_date
        UNION ALL
        SELECT product_code, operation_timestamp
        FROM logs.product_discount_changes_log
        WHERE operation_timestamp BETWEEN start_date AND end_date
    ),
    changes_count AS (
        SELECT ac.product_code, COUNT(*) AS change_count
        FROM all_changes ac
        GROUP BY ac.product_code
    )
    SELECT p.product_code, p.product_name, c.change_count
    FROM changes_count c
    JOIN production.products p ON c.product_code = p.product_code
    ORDER BY c.change_count DESC;
END;
$$ LANGUAGE plpgsql;



DROP FUNCTION IF EXISTS most_profitable_products(DATE);
CREATE OR REPLACE FUNCTION most_profitable_products(month_date DATE)
RETURNS TABLE(product_code VARCHAR, total_profit NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT
        od.product_code,
        SUM(
            (od.price_each - COALESCE(ob.buy_price, 0) -
            CASE
                WHEN pd.discount_unit = 'P' THEN (pd.discount_value / 100.0) * od.price_each
                WHEN pd.discount_unit = 'A' THEN pd.discount_value
                ELSE 0
            END) * od.quantity_ordered
        )::numeric(10, 2) AS total_profit
    FROM
        order_details od
    JOIN
        orders o ON od.order_number = o.order_number
    LEFT JOIN
        office_buys ob ON od.product_code = ob.product_code
    LEFT JOIN
        production.products_discount pd ON od.product_code = pd.product_code
        AND o.order_date BETWEEN pd.date_created AND pd.valid_until
        AND pd.in_active =TRUE
    WHERE
        DATE_TRUNC('month', o.shipped_date) = DATE_TRUNC('month', month_date)
      AND o.status = 'Shipped'
    GROUP BY
        od.product_code
    HAVING
        SUM(
            (od.price_each - COALESCE(ob.buy_price, 0) -
            CASE
                WHEN pd.discount_unit = 'P' THEN (pd.discount_value / 100.0) * od.price_each
                WHEN pd.discount_unit = 'A' THEN pd.discount_value
                ELSE 0
            END) * od.quantity_ordered
        ) > 0
    ORDER BY
        total_profit DESC;
END;
$$ LANGUAGE plpgsql;
