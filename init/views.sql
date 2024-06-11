-- Create a view named monthly_active_users to aggregate data about monthly active users based on their orders
CREATE  OR REPLACE VIEW monthly_active_users AS
SELECT
    c.customer_number,
    c.city,
    TO_CHAR(DATE_TRUNC('month', o.shipped_date), 'YYYY-Month') AS active_month,
    COUNT(DISTINCT o.order_number) AS orders_count
FROM
    customers c
JOIN
    orders o ON c.customer_number = o.customer_number
WHERE
    o.status = 'Shipped'
GROUP BY
    c.customer_number, c.city, active_month
HAVING
    COUNT(DISTINCT o.order_number) >= 1;


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

-- This view calculates product vendor where there is exactly one order per month.
CREATE OR REPLACE VIEW single_order_brands_per_month AS
SELECT
    p.product_vendor,
    TO_CHAR(DATE_TRUNC('month', o.shipped_date), 'YYYY-Month') AS order_month

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
    1 >= COUNT(o.order_number);


