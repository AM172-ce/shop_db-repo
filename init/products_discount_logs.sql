-- Modify the log table to store old and new data directly for product discount changes
CREATE TABLE IF NOT EXISTS logs.product_discount_changes_log (
    log_id SERIAL PRIMARY KEY,
    product_code VARCHAR(15) NOT NULL,
    operation_type VARCHAR(10) NOT NULL,
    operation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    old_discount_value NUMERIC(10, 2),
    old_discount_unit VARCHAR(1),
    old_date_created TIMESTAMP,
    old_valid_until TIMESTAMP,
    old_discount_description TEXT,
    new_discount_value NUMERIC(10, 2),
    new_discount_unit VARCHAR(1),
    new_date_created TIMESTAMP,
    new_valid_until TIMESTAMP,
    new_discount_description TEXT
);

CREATE OR REPLACE FUNCTION logs.log_product_discount_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO logs.product_discount_changes_log (product_code, operation_type, user_id, old_discount_value, old_discount_unit, old_date_created, old_valid_until, old_discount_description)
        VALUES (OLD.product_code, 'DELETE', current_user, OLD.discount_value, OLD.discount_unit, OLD.date_created, OLD.valid_until, OLD.discount_description);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO logs.product_discount_changes_log (product_code, operation_type, user_id, old_discount_value, old_discount_unit, old_date_created, old_valid_until, old_discount_description, new_discount_value, new_discount_unit, new_date_created, new_valid_until, new_discount_description)
        VALUES (NEW.product_code, 'UPDATE', current_user, OLD.discount_value, OLD.discount_unit, OLD.date_created, OLD.valid_until, OLD.discount_description, NEW.discount_value, NEW.discount_unit, NEW.date_created, NEW.valid_until, NEW.discount_description);
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO logs.product_discount_changes_log (product_code, operation_type, user_id, new_discount_value, new_discount_unit, new_date_created, new_valid_until, new_discount_description)
        VALUES (NEW.product_code, 'INSERT', current_user, NEW.discount_value, NEW.discount_unit, NEW.date_created, NEW.valid_until, NEW.discount_description);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS product_discount_changes_trigger ON production.products_discount;
CREATE TRIGGER product_discount_changes_trigger
AFTER INSERT OR UPDATE OR DELETE ON production.products_discount
FOR EACH ROW EXECUTE FUNCTION logs.log_product_discount_changes();
