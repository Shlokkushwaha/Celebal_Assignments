-- ====================================================
-- DATA ENGINEERING ASSIGNMENT 003
-- Superstore Sales Analysis
-- ====================================================

-- ====================================================
-- STEP 1: Create Database
-- ====================================================

CREATE DATABASE super_store;
USE super_store;

-- ====================================================
-- STEP 2: Create Raw Table
-- This table stores the imported Superstore dataset
-- ====================================================

CREATE TABLE superstore_raw (
row_id INT,
order_id VARCHAR(50),
order_date VARCHAR(50),
ship_date VARCHAR(50),
ship_mode VARCHAR(50),
customer_id VARCHAR(50),
customer_name VARCHAR(100),
segment VARCHAR(50),
country VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
postal_code VARCHAR(20),
region VARCHAR(50),
product_id VARCHAR(50),
category VARCHAR(50),
sub_category VARCHAR(50),
product_name VARCHAR(255),
sales DECIMAL(10,2),
quantity INT,
discount DECIMAL(5,2),
profit DECIMAL(10,2)
);

-- ====================================================
-- Verify Dataset Import
-- ====================================================

SELECT COUNT(*) AS total_records
FROM superstore_raw;

-- ====================================================
-- STEP 3: Create Customers Table
-- Using SELECT DISTINCT to avoid duplicate customers
-- ====================================================

CREATE TABLE customers AS
SELECT DISTINCT
customer_id,
customer_name,
segment
FROM superstore_raw;

SELECT *
FROM customers
LIMIT 10;

-- ====================================================
-- STEP 4: Create Products Table
-- Using SELECT DISTINCT to avoid duplicate products
-- ====================================================

CREATE TABLE products AS
SELECT DISTINCT
product_id,
product_name,
category,
sub_category
FROM superstore_raw;

SELECT *
FROM products
LIMIT 10;

-- ====================================================
-- STEP 5: Create Orders Table
-- Contains transactional order information
-- ====================================================

CREATE TABLE orders AS
SELECT DISTINCT
order_id,
order_date,
ship_date,
customer_id,
product_id,
sales,
quantity,
profit
FROM superstore_raw;

SELECT *
FROM orders
LIMIT 10;

-- ====================================================
-- SUBQUERY 1
-- Orders with Sales Greater than Average Sales
-- ====================================================

SELECT *
FROM orders
WHERE sales >
(
SELECT AVG(sales)
FROM orders
);

-- ====================================================
-- SUBQUERY 2
-- Highest Sale Order for Each Customer
-- ====================================================

SELECT *
FROM orders o
WHERE sales =
(
SELECT MAX(sales)
FROM orders
WHERE customer_id = o.customer_id
);

-- ====================================================
-- CTE 1
-- Calculate Total Sales Per Customer
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
)

SELECT *
FROM customer_sales;

-- ====================================================
-- CTE 2
-- Customers with Above Average Total Sales
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
)

SELECT *
FROM customer_sales
WHERE total_sales >
(
SELECT AVG(total_sales)
FROM customer_sales
);

-- ====================================================
-- WINDOW FUNCTION 1
-- ROW_NUMBER()
-- Assigns a unique rank within each customer
-- ====================================================

SELECT
customer_id,
sales,
ROW_NUMBER() OVER
(
PARTITION BY customer_id
ORDER BY sales DESC
) AS rn
FROM orders;

-- ====================================================
-- WINDOW FUNCTION 2
-- RANK()
-- Ranks sales within each customer group
-- ====================================================

SELECT
customer_id,
sales,
RANK() OVER
(
PARTITION BY customer_id
ORDER BY sales DESC
) AS ranking
FROM orders;

-- ====================================================
-- BUSINESS QUERY 1
-- Top 10 Customers by Total Sales
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
)

SELECT
customer_id,
total_sales
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 10;

-- ====================================================
-- BUSINESS QUERY 2
-- Top 10 Customers with Customer Names
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
)

SELECT
c.customer_name,
cs.total_sales
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY total_sales DESC
LIMIT 10;

-- ====================================================
-- BUSINESS QUERY 3
-- Customers Who Placed Only One Order
-- ====================================================

SELECT
customer_id,
COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) = 1;

-- ====================================================
-- BUSINESS QUERY 4
-- Customers with Above Average Total Sales
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
)

SELECT *
FROM customer_sales
WHERE total_sales >
(
SELECT AVG(total_sales)
FROM customer_sales
);

-- ====================================================
-- FINAL QUERY
-- JOIN + CTE + WINDOW FUNCTION
-- Top Ranked Customers by Sales
-- ====================================================

WITH customer_sales AS
(
SELECT
customer_id,
SUM(sales) AS total_sales
FROM orders
GROUP BY customer_id
),

ranked_customers AS
(
SELECT
customer_id,
total_sales,
RANK() OVER
(
ORDER BY total_sales DESC
) AS rank_no
FROM customer_sales
)

SELECT
c.customer_name,
rc.total_sales,
rc.rank_no
FROM ranked_customers rc
JOIN customers c
ON rc.customer_id = c.customer_id
WHERE rank_no <= 10;


-- ====================================================
-- WINDOW FUNCTION
-- Top 3 Customers Based on Total Sales
-- ====================================================

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
),

ranked_customers AS
(
    SELECT
        customer_id,
        total_sales,
        RANK() OVER
        (
            ORDER BY total_sales DESC
        ) AS customer_rank
    FROM customer_sales
)

SELECT *
FROM ranked_customers
WHERE customer_rank <= 3;

-- ====================================================
-- Bottom 5 Customers Based on Total Sales
-- ====================================================

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.customer_name,
    cs.total_sales
FROM customer_sales cs
JOIN customers c
    ON cs.customer_id = c.customer_id
ORDER BY total_sales ASC
LIMIT 5;

-- ====================================================
-- Rank All Customers Based on Total Sales
-- ====================================================

WITH customer_sales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_sales,
    RANK() OVER
    (
        ORDER BY total_sales DESC
    ) AS customer_rank
FROM customer_sales;
-- ====================================================
-- END OF ASSIGNMENT
-- ====================================================
