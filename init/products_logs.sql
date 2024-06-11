-- Modify the log table to store old and new data directly
CREATE TABLE IF NOT EXISTS logs.product_changes_log (
    log_id SERIAL PRIMARY KEY,
    product_code VARCHAR(15) NOT NULL,
    operation_type VARCHAR(10) NOT NULL,
    operation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    old_product_name VARCHAR(70),
    old_product_vendor VARCHAR(50),
    old_product_description TEXT,
    old_quantity_in_stock BIGINT,
    old_product_category_code VARCHAR(15),
    new_product_name VARCHAR(70),
    new_product_vendor VARCHAR(50),
    new_product_description TEXT,
    new_quantity_in_stock BIGINT,
    new_product_category_code VARCHAR(15)
);

CREATE OR REPLACE FUNCTION logs.log_product_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO logs.product_changes_log (product_code, operation_type, user_id, old_product_name, old_product_vendor, old_product_description, old_quantity_in_stock, old_product_category_code)
        VALUES (OLD.product_code, 'DELETE', current_user, OLD.product_name, OLD.product_vendor, OLD.product_description, OLD.quantity_in_stock, OLD.product_category_code);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO logs.product_changes_log (product_code, operation_type, user_id, old_product_name, old_product_vendor, old_product_description, old_quantity_in_stock, old_product_category_code, new_product_name, new_product_vendor, new_product_description, new_quantity_in_stock, new_product_category_code)
        VALUES (NEW.product_code, 'UPDATE', current_user, OLD.product_name, OLD.product_vendor, OLD.product_description, OLD.quantity_in_stock, OLD.product_category_code, NEW.product_name, NEW.product_vendor, NEW.product_description, NEW.quantity_in_stock, NEW.product_category_code);
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO logs.product_changes_log (product_code, operation_type, user_id, new_product_name, new_product_vendor, new_product_description, new_quantity_in_stock, new_product_category_code)
        VALUES (NEW.product_code, 'INSERT', current_user, NEW.product_name, NEW.product_vendor, NEW.product_description, NEW.quantity_in_stock, NEW.product_category_code);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS products_changes_trigger ON production.products;
CREATE TRIGGER products_changes_trigger
AFTER INSERT OR UPDATE OR DELETE ON production.products
FOR EACH ROW EXECUTE FUNCTION logs.log_product_changes();
