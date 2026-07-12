
-- Query 1 - Total Customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- Query 2 - Total Products
SELECT COUNT(*) AS total_products
FROM products;

-- Query 3 - Total Orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Query 4 - Total Revenue
SELECT
SUM(quantity * unit_price * (1-discount_percent/100.0))
AS total_revenue
FROM order_items;

-- Query 5 - Top 10 Selling Products
SELECT

p.product_name,

SUM(oi.quantity) AS total_quantity

FROM order_items oi

JOIN products p

ON oi.product_id = p.product_id

GROUP BY p.product_name

ORDER BY total_quantity DESC

LIMIT 10;

-- Query 6 - Revenue by Category
SELECT

p.category,

ROUND(
SUM(
oi.quantity *
oi.unit_price *
(1-oi.discount_percent/100.0)
),2
) AS revenue

FROM order_items oi

JOIN products p

ON oi.product_id=p.product_id

GROUP BY p.category

ORDER BY revenue DESC;

-- Query 7 - Orders by Status
SELECT

status,

COUNT(*) AS total_orders

FROM orders

GROUP BY status;

-- Query 8 - Customers by Type
SELECT

customer_type,

COUNT(*) AS total

FROM customers

GROUP BY customer_type;

-- Query 9 - Top 10 Customers by Spending
SELECT

c.customer_name,

ROUND(
SUM(
oi.quantity *
oi.unit_price *
(1-oi.discount_percent/100.0)
),2
) AS total_spent

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY c.customer_name

ORDER BY total_spent DESC

LIMIT 10;

-- Query 10 - Region Wise Order
SELECT

region_code,

COUNT(*) AS total_orders

FROM orders

GROUP BY region_code;

-- Query 11 - Average Order Value
SELECT

ROUND(
AVG(order_total),2
) AS average_order_value

FROM(

SELECT

order_id,

SUM(
quantity*
unit_price*
(1-discount_percent/100.0)
) AS order_total

FROM order_items

GROUP BY order_id

);

-- Query 12 - Returned Items
SELECT

COUNT(*) AS total_returns

FROM order_items

WHERE is_return=1;

-- Query 13 - Most Expensive Products
SELECT

product_name,

cost_price

FROM products

ORDER BY cost_price DESC

LIMIT 10;

-- Query 14 - Average Discount
SELECT

ROUND(
AVG(discount_percent),2
)

AS average_discount

FROM order_items;

-- Query 15 - Customer Registration by Year

SELECT

strftime('%Y',registration_date) AS year,

COUNT(*) AS total

FROM customers

GROUP BY year;

-- Highest Revenue Region
SELECT

o.region_code,

ROUND(
SUM(
oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)
),2
)

AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY o.region_code

ORDER BY revenue DESC;


-- Average Discount per Category
SELECT

p.category,

ROUND(
AVG(oi.discount_percent),2
)

AS avg_discount

FROM order_items oi

JOIN products p

ON oi.product_id=p.product_id

GROUP BY p.category;


-- Query 16 - Customers with No Orders

SELECT
c.customer_id,
c.customer_name
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


-- Query 17 - Products Never Ordered

SELECT
p.product_id,
p.product_name
FROM products p
LEFT JOIN order_items oi
ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- Query 18 - Monthly Revenue

WITH MonthlyRevenue AS (

SELECT

strftime('%Y-%m', o.order_date) AS month,

SUM(
oi.quantity *
oi.unit_price *
(1 - oi.discount_percent/100.0)
) AS revenue

FROM orders o

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY month

)

SELECT *
FROM MonthlyRevenue
ORDER BY month;

-- Query 19 - Product Ranking

SELECT

product_name,

total_quantity,

RANK() OVER(
ORDER BY total_quantity DESC
) AS product_rank

FROM(

SELECT

p.product_name,

SUM(oi.quantity) AS total_quantity

FROM order_items oi

JOIN products p
ON oi.product_id = p.product_id

GROUP BY p.product_name

);


-- Query 20 - Customer Row Number

SELECT

customer_name,

customer_type,

ROW_NUMBER() OVER(
ORDER BY customer_name
) AS row_num

FROM customers;


-- Query 21 - Customer Spending Rank

SELECT

customer_name,

total_spent,

DENSE_RANK() OVER(
ORDER BY total_spent DESC
) AS spending_rank

FROM(

SELECT

c.customer_name,

SUM(
oi.quantity *
oi.unit_price *
(1-oi.discount_percent/100.0)
) AS total_spent

FROM customers c

JOIN orders o
ON c.customer_id=o.customer_id

JOIN order_items oi
ON o.order_id=oi.order_id

GROUP BY c.customer_name

);


-- Query 22 - Running Revenue

SELECT

order_id,

SUM(
quantity *
unit_price *
(1-discount_percent/100.0)
)

OVER(

ORDER BY order_id

ROWS BETWEEN UNBOUNDED PRECEDING
AND CURRENT ROW

) AS running_revenue

FROM order_items;


-- Query 23 - Customer Segments

SELECT

customer_name,

NTILE(4) OVER(
ORDER BY customer_name
) AS customer_group

FROM customers;

-- Query 24 - Previous Order Date

SELECT

order_id,

order_date,

LAG(order_date)

OVER(
ORDER BY order_date
)

AS previous_order

FROM orders;

-- Query 25 - Next Order Date

SELECT

order_id,

order_date,

LEAD(order_date)

OVER(
ORDER BY order_date
)

AS next_order

FROM orders;