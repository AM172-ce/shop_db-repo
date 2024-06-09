CREATE TABLE IF NOT EXISTS offices
(
    office_code   VARCHAR(10) NOT NULL
        PRIMARY KEY,
    city          VARCHAR(50) NOT NULL,
    phone         VARCHAR(50) NOT NULL,
    address_line1 VARCHAR(50) NOT NULL,
    address_line2 VARCHAR(50),
    state         VARCHAR(50),
    country       VARCHAR(50) NOT NULL,
    postal_code   VARCHAR(15) NOT NULL,
    territory     VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS employees
(
    employee_number BIGINT       NOT NULL
        PRIMARY KEY,
    lastname        VARCHAR(50)  NOT NULL,
    firstname       VARCHAR(50)  NOT NULL,
    extension       VARCHAR(10)  NOT NULL,
    email           VARCHAR(100) NOT NULL,
    office_code     VARCHAR(10)  NOT NULL
        CONSTRAINT employees_fk_1
            REFERENCES offices,
    reports_to      BIGINT
        CONSTRAINT employees_fk_2
            REFERENCES employees,
    job_title       VARCHAR(50)  NOT NULL
);


CREATE TABLE IF NOT EXISTS customers
(
    customer_number       BIGINT      NOT NULL
        PRIMARY KEY,
    contact_lastname      VARCHAR(50),
    contact_firstname     VARCHAR(50),
    phone                 VARCHAR(50) NOT NULL,
    address_line1         VARCHAR(50) NOT NULL,
    address_line2         VARCHAR(50),
    city                  VARCHAR(50),
    state                 VARCHAR(50),
    postal_code           VARCHAR(15),
    country               VARCHAR(60) NOT NULL,
    sales_employee_number BIGINT
        CONSTRAINT customers_fk_1
            REFERENCES employees,
    credit_limit          NUMERIC(10, 2)
);


CREATE TABLE IF NOT EXISTS orders
(
    order_number    BIGINT      NOT NULL
        PRIMARY KEY,
    order_date      TIMESTAMP   NOT NULL,
    required_date   TIMESTAMP   NOT NULL,
    shipped_date    TIMESTAMP,
    status          VARCHAR(15) NOT NULL,
    comments        TEXT,
    customer_number BIGINT      NOT NULL
        CONSTRAINT orders_fk_1
            REFERENCES customers
);


CREATE TABLE IF NOT EXISTS payments
(
    customer_number BIGINT         NOT NULL
        CONSTRAINT payments_fk_1
            REFERENCES customers,
    check_number    VARCHAR(50)    NOT NULL,
    payment_date    TIMESTAMP      NOT NULL,
    amount          NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (customer_number, check_number)
);


CREATE TABLE IF NOT EXISTS production.product_categories
(
    product_category_code        VARCHAR(15) NOT NULL
        PRIMARY KEY,
    category_name                VARCHAR(70) NOT NULL,
    product_category_description TEXT,
    parent_category_code         VARCHAR(15)
        CONSTRAINT product_categories_fk_1
            REFERENCES production.product_categories
);


CREATE TABLE IF NOT EXISTS production.products
(
    product_code          VARCHAR(15) NOT NULL
        PRIMARY KEY,
    product_name          VARCHAR(70) NOT NULL,
    product_vendor        VARCHAR(50) NOT NULL,
    product_description   TEXT        NOT NULL,
    quantity_in_stock     BIGINT      NOT NULL,
    product_category_code VARCHAR(15)
        CONSTRAINT products_fk_1
            REFERENCES production.product_categories
);

CREATE TABLE IF NOT EXISTS production.products_comments
(
    product_code    VARCHAR(15) NOT NULL
        REFERENCES production.products,
    customer_number BIGINT      NOT NULL
        REFERENCES customers,
    comments        TEXT,
    rates           integer     NOT NULL,
    PRIMARY KEY (product_code, customer_number)
);


CREATE TABLE IF NOT EXISTS production.discount_units
(
    discount_unit_code VARCHAR(1) NOT NULL
        PRIMARY KEY,
    discount_unit_name VARCHAR(15)
);


CREATE TABLE IF NOT EXISTS production.products_discount
(
    product_discount_code BIGINT         NOT NULL
        CONSTRAINT product_discount_pk
            PRIMARY KEY,
    product_code          VARCHAR(15)    NOT NULL
        CONSTRAINT product_discount_fk_1
            REFERENCES production.products,
    discount_value        NUMERIC(10, 2) NOT NULL,
    discount_unit         VARCHAR(1)     NOT NULL
        CONSTRAINT products_discount_fk_2
            REFERENCES production.discount_units,
   date_created           TIMESTAMP      NOT NULL,
    valid_until           TIMESTAMP      NOT NULL,
    discount_description  TEXT,
    CONSTRAINT product_discount_unique UNIQUE (product_code,date_created, valid_until)
);

CREATE TABLE IF NOT EXISTS production.product_categories_discount
(
    product_categories_discount_code BIGINT         NOT NULL
        PRIMARY KEY,
    product_categories_code          VARCHAR(15)    NOT NULL
        CONSTRAINT product_categories_discount_fk_1
            REFERENCES production.product_categories,
    discount_value                   NUMERIC(10, 2) NOT NULL,
    discount_unit                    VARCHAR(1)     NOT NULL
        CONSTRAINT product_categories_discount_fk_2
            REFERENCES production.discount_units,
    date_created                     TIMESTAMP      NOT NULL,
    valid_until                      TIMESTAMP      NOT NULL,
    discount_description             TEXT,
    CONSTRAINT product_categories_discount_unique UNIQUE (product_categories_code, date_created, valid_until)
);


CREATE TABLE IF NOT EXISTS production.products_pricing
(
    products_pricing_code BIGINT         NOT NULL
        PRIMARY KEY,
    products_code         VARCHAR(15)    NOT NULL
        CONSTRAINT products_pricing_fk_1
            REFERENCES production.products,
    base_price            NUMERIC(10, 2) NOT NULL,
    date_created          TIMESTAMP      NOT NULL,
    date_expiry           TIMESTAMP,
    in_active             boolean        NOT NULL,
    msrp                  NUMERIC(10, 2) NOT NULL,
    CONSTRAINT chk_one_active_record_per_product
        check ((in_active = false) OR ((in_active = true) AND (date_expiry IS NULL)))
);

CREATE TABLE IF NOT EXISTS order_details
(
    order_number      BIGINT         NOT NULL
        CONSTRAINT order_details_fk_1
            REFERENCES orders,
    product_code      VARCHAR(15)    NOT NULL
        CONSTRAINT order_details_fk_2
            REFERENCES production.products,
    quantity_ordered  BIGINT         NOT NULL,
    price_each        NUMERIC(10, 2) NOT NULL,
    order_line_number integer        NOT NULL,
    PRIMARY KEY (order_number, product_code)
);

CREATE TABLE IF NOT EXISTS office_buys
(
    office_buy_code BIGINT generated always as identity
        CONSTRAINT office_buys_pk
            PRIMARY KEY,
    buy_date       TIMESTAMP,
    product_code    VARCHAR(15)
        CONSTRAINT office_buys_fk_1
            REFERENCES production.products,
    buy_quantity    BIGINT,
    buy_price       NUMERIC(10, 2),
    office_code     VARCHAR(10)
        CONSTRAINT office_buys_fk_2
            REFERENCES offices
);