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
