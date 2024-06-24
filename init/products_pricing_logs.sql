-- Modify the log table to store old and new data directly for product pricing changes
CREATE TABLE IF NOT EXISTS logs.product_pricing_changes_log (
    log_id SERIAL PRIMARY KEY,
    product_code VARCHAR(15) NOT NULL,
    operation_type VARCHAR(10) NOT NULL,
    operation_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(50),
    old_base_price NUMERIC(10, 2),
    old_date_created TIMESTAMP,
    old_date_expiry TIMESTAMP,
    old_in_active BOOLEAN,
    old_msrp NUMERIC(10, 2),
    new_base_price NUMERIC(10, 2),
    new_date_created TIMESTAMP,
    new_date_expiry TIMESTAMP,
    new_in_active BOOLEAN,
    new_msrp NUMERIC(10, 2)
);

CREATE OR REPLACE FUNCTION logs.log_product_pricing_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO logs.product_pricing_changes_log (product_code, operation_type, user_id, old_base_price, old_date_created, old_date_expiry, old_in_active, old_msrp)
        VALUES (OLD.product_code, 'DELETE', current_user, OLD.base_price, OLD.date_created, OLD.date_expiry, OLD.in_active, OLD.msrp);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO logs.product_pricing_changes_log (product_code, operation_type, user_id, old_base_price, old_date_created, old_date_expiry, old_in_active, old_msrp, new_base_price, new_date_created, new_date_expiry, new_in_active, new_msrp)
        VALUES (NEW.product_code, 'UPDATE', current_user, OLD.base_price, OLD.date_created, OLD.date_expiry, OLD.in_active, OLD.msrp, NEW.base_price, NEW.date_created, NEW.date_expiry, NEW.in_active, NEW.msrp);
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO logs.product_pricing_changes_log (product_code, operation_type, user_id, new_base_price, new_date_created, new_date_expiry, new_in_active, new_msrp)
        VALUES (NEW.product_code, 'INSERT', current_user, NEW.base_price, NEW.date_created, NEW.date_expiry, NEW.in_active, NEW.msrp);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS product_pricing_changes_trigger ON production.products_pricing;
CREATE TRIGGER product_pricing_changes_trigger
AFTER INSERT OR UPDATE OR DELETE ON production.products_pricing
FOR EACH ROW EXECUTE FUNCTION logs.log_product_pricing_changes();
