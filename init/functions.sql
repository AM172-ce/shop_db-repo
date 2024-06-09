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
            TO_CHAR(DATE_TRUNC(''month''::text, o.order_date::timestamp without time zone), ''Month'') AS order_month,
            COUNT(DISTINCT o.order_number) AS orders_count
        FROM
            customers c
        JOIN
            orders o ON c.customer_number = o.customer_number
        WHERE
            o.status = ''Shipped''
            AND c.city = ''%s''
        GROUP BY
            c.customer_number, c.city, order_month
        HAVING
            COUNT(DISTINCT o.order_number) >= 1;
    ', city_name, city_name);

END
$$ LANGUAGE plpgsql;


--Function to retrieve a report of product changes within a specified time frame.
CREATE OR REPLACE FUNCTION production.get_product_changes_report(start_date TIMESTAMP, end_date TIMESTAMP)
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