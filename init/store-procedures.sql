-- This procedure loads data into multiple tables from CSV files located in a base directory.
CREATE OR REPLACE PROCEDURE load_all_tables()
LANGUAGE plpgsql
AS $$
DECLARE
    base_path TEXT := '/mnt/shared/data/';
BEGIN
    PERFORM load_table_from_csv('public', 'offices', base_path || 'offices.csv');

    PERFORM load_table_from_csv('public', 'employees', base_path || 'employees.csv');

    PERFORM load_table_from_csv('public', 'customers', base_path || 'customers.csv');

    PERFORM load_table_from_csv('public', 'orders', base_path || 'orders.csv');

    PERFORM load_table_from_csv('public', 'payments', base_path || 'payments.csv');

    PERFORM load_table_from_csv('production', 'product_categories', base_path || 'product_categories.csv');

    PERFORM load_table_from_csv('production', 'products', base_path || 'products.csv');

    PERFORM load_table_from_csv('production', 'products_comments', base_path || 'products_comments.csv');

    PERFORM load_table_from_csv('production', 'discount_units', base_path || 'discount_units.csv');

    PERFORM load_table_from_csv('production', 'products_discount', base_path || 'products_discount.csv');

    PERFORM load_table_from_csv('production', 'product_categories_discount', base_path || 'product_categories_discount.csv');

    PERFORM load_table_from_csv('production', 'products_pricing', base_path || 'products_pricing.csv');

    PERFORM load_table_from_csv('public', 'order_details', base_path || 'order_details.csv');

    PERFORM load_table_from_csv('public', 'office_buys', base_path || 'office_buys.csv');
END;
$$;

--store-procedure to calculate yearly customers who had the most discounts.
CREATE OR REPLACE PROCEDURE calculate_yearly_customer_discounts()
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS temp_yearly_customer_discounts;
    CREATE TEMP TABLE temp_yearly_customer_discounts (
        customer_number INT,
        contact_firstname VARCHAR,
        contact_lastname VARCHAR,
        total_discount NUMERIC(10, 2)
    );

    INSERT INTO temp_yearly_customer_discounts
    SELECT
        c.customer_number,
        c.contact_firstname,
        c.contact_lastname,
        SUM(
            CASE
                WHEN pd.discount_unit = 'P' THEN ((pd.discount_value / 100.0) * od.price_each) * od.quantity_ordered
                WHEN pd.discount_unit = 'A' THEN pd.discount_value * od.quantity_ordered
                ELSE 0
            END
        )::numeric(10, 2) AS total_discount
    FROM
        customers c
    JOIN
        orders o ON c.customer_number = o.customer_number
    JOIN
        order_details od ON o.order_number = od.order_number
    LEFT JOIN
        production.products_discount pd ON od.product_code = pd.product_code
        AND o.order_date BETWEEN pd.date_created AND pd.valid_until
        AND pd.in_active =TRUE
    WHERE
        o.status = 'Shipped'
        AND o.shipped_date BETWEEN CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE
    GROUP BY
        c.customer_number
    HAVING
        SUM(
            CASE
                WHEN pd.discount_unit = 'P' THEN ((pd.discount_value / 100.0) * od.price_each) * od.quantity_ordered
                WHEN pd.discount_unit = 'A' THEN pd.discount_value * od.quantity_ordered
                ELSE 0
            END
        ) != 0
    ORDER BY
        total_discount DESC;
END;
$$;


CALL calculate_yearly_customer_discounts();

SELECT * FROM temp_yearly_customer_discounts;


CREATE OR REPLACE PROCEDURE get_most_profitable_products(IN the_date date)
    language plpgsql
AS
$$
DECLARE
    record RECORD;
BEGIN
    DROP TABLE IF EXISTS temp_most_profitable_products;
    CREATE TEMP TABLE temp_most_profitable_products (
        product_code VARCHAR,
        total_profit NUMERIC
    );

  
    FOR record IN
        SELECT * FROM most_profitable_products(the_date)
    LOOP
        INSERT INTO temp_most_profitable_products (product_code, total_profit)
        VALUES (record.product_code, record.total_profit);

        
        RAISE NOTICE 'Product Code: %, Total Profit: %', record.product_code, record.total_profit;
    END LOOP;
END;
$$;

CALL get_most_profitable_products('2024-5-6');
SELECT * FROM temp_most_profitable_products;




