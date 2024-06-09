-- Create a view named monthly_active_users to aggregate data about monthly active users based on their orders
CREATE  OR REPLACE VIEW monthly_active_users AS
SELECT
    c.customer_number,
    c.city,
    TO_CHAR(DATE_TRUNC('month'::text, o.order_date::timestamp without time zone), 'Month- YYYY') AS order_month,
    COUNT(DISTINCT o.order_number) AS orders_count
FROM
    customers c
JOIN
    orders o ON c.customer_number = o.customer_number
WHERE
    o.status = 'Shipped'
GROUP BY
    c.customer_number, c.city, order_month
HAVING
    COUNT(DISTINCT o.order_number) >= 1;

-- The view lists the top 10 customers who have made the most purchases in the first half of the year 2024.
CREATE OR REPLACE VIEW top_customers_with_most_purchases_first_half_year AS
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
    o.order_date BETWEEN '2024-01-01 00:00:00' AND '2024-06-30 23:59:59'
    AND o.status = 'Shipped'
GROUP BY
    c.customer_number, c.contact_firstname
ORDER BY
    total_orders DESC
LIMIT 10;

-- Create a view that lists the least interested brands based on the total number of orders.
-- The view will display the top 10 vendors with the fewest shipped orders.
CREATE OR REPLACE VIEW least_interested_brands AS
SELECT
    p.product_vendor,
    COUNT(o.order_number) AS total_orders
FROM
    production.products p
LEFT JOIN
    order_details od ON p.product_code = od.product_code
LEFT JOIN
    orders o ON od.order_number = o.order_number
    AND o.status = 'Shipped'
GROUP BY
    p.product_vendor
ORDER BY
    total_orders ASC
LIMIT 10;

-- This view calculates the number of orders per month for each product vendor where there is exactly one order per month.
CREATE OR REPLACE VIEW single_order_brands_per_month AS
SELECT
    p.product_vendor,
    TO_CHAR(DATE_TRUNC('month', o.order_date), 'Month-YYYY') AS order_month,
    COUNT(DISTINCT o.order_number) AS total_orders
FROM
    production.products p
JOIN
    order_details od ON p.product_code = od.product_code
JOIN
    orders o ON od.order_number = o.order_number
    AND o.status = 'Shipped'
GROUP BY
    p.product_vendor, order_month
HAVING
    COUNT(DISTINCT o.order_number) = 1;

/*
View to calculate the monthly profit by city.
Description:
This view calculates the total profit from all products for each city every month,
considering any discounts applied to those products.
The profit is calculated as the difference between the selling price and the buy price,
adjusted for any discounts applied. The results are grouped by city and month.
*/

CREATE OR REPLACE VIEW monthly_profit_by_city AS
SELECT
    c.city,
    TO_CHAR(DATE_TRUNC('month', o.order_date), 'YYYY-MM') AS order_month,
    SUM(
        (od.price_each - COALESCE(ob.buy_price, 0) -
        CASE
            WHEN pd.discount_unit = 'P' THEN (pd.discount_value / 100.0) * od.price_each
            WHEN pd.discount_unit = 'A' THEN pd.discount_value
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
    AND pd.valid_until >= o.order_date
LEFT JOIN
    office_buys ob ON od.product_code = ob.product_code
WHERE
    o.status = 'Shipped'
GROUP BY
    c.city, DATE_TRUNC('month', o.order_date)
ORDER BY
    c.city, order_month, total_profit DESC;


--View to calculate yearly customers who had the most discounts.
CREATE OR REPLACE VIEW yearly_customer_discounts AS
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
    AND pd.valid_until >= o.order_date
WHERE
    o.status = 'Shipped'
    AND o.order_date BETWEEN CURRENT_DATE - INTERVAL '1 year' AND CURRENT_DATE
GROUP BY
    c.customer_number, c.contact_firstname
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