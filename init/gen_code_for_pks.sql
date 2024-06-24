CREATE OR REPLACE FUNCTION generate_char_number_code()
RETURNS VARCHAR AS $$
DECLARE
    code VARCHAR(5);
    letters VARCHAR(2);
BEGIN

    letters := chr(65 + floor(random() * 26)::int) || chr(65 + floor(random() * 26)::int);
    code := letters || lpad(cast(floor(random() * 1000)::int as varchar), 3, '0');
    RETURN code;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION generate_numeric_code()
RETURNS BIGINT AS $$
DECLARE
    code BIGINT;
BEGIN
    code := (random() * 999999 + 100000)::BIGINT;
    RETURN code;
END;
$$ LANGUAGE plpgsql;


--product code
CREATE OR REPLACE FUNCTION set_product_code()
RETURNS TRIGGER AS $$
BEGIN
    LOOP
        NEW.product_code := generate_char_number_code();

        IF NOT EXISTS (SELECT 1 FROM production.products WHERE product_code = NEW.product_code) THEN
            RETURN NEW;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_insert_product ON production.products;
CREATE TRIGGER before_insert_product
BEFORE INSERT ON production.products
FOR EACH ROW EXECUTE FUNCTION set_product_code();


--product pricing code
CREATE OR REPLACE FUNCTION set_pricing_code() RETURNS TRIGGER AS $$
BEGIN
    LOOP
        NEW.products_pricing_code := generate_numeric_code();
    IF NOT EXISTS (SELECT 1 FROM production.products_pricing WHERE products_pricing_code = NEW.products_pricing_code) THEN
        RETURN NEW;
    END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_insert_pricing ON production.products_pricing;
CREATE TRIGGER before_insert_pricing
BEFORE INSERT ON production.products_pricing
FOR EACH ROW
EXECUTE FUNCTION set_pricing_code();

--product discount code
CREATE OR REPLACE FUNCTION set_discount_code() RETURNS TRIGGER AS $$
BEGIN
    LOOP
        NEW.product_discount_code := generate_numeric_code();
    IF NOT EXISTS (SELECT 1 FROM production.products_discount WHERE product_discount_code = NEW.product_discount_code) THEN
        RETURN NEW;
    END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_insert_p_discount ON production.products_discount;
CREATE TRIGGER before_insert_p_discount
BEFORE INSERT ON production.products_discount
FOR EACH ROW
EXECUTE FUNCTION set_discount_code();


