-- =====================================================
-- DATABASE CREATION
-- =====================================================

CREATE DATABASE shopease;
USE shopease;

SHOW DATABASES;

-- =====================================================
-- TABLE CREATION
-- =====================================================

-- Customer Master Table
CREATE TABLE customers(
	customer_id   INT PRIMARY KEY,
    first_name    VARCHAR(50) NOT NULL,
    last_name     VARCHAR(50) NOT NULL,
    email         VARCHAR(100) UNIQUE NOT NULL,
    city          VARCHAR(50) NOT NULL,
    state         VARCHAR(50) NOT NULL,
    join_date     DATE NOT NULL,
    is_premium    BOOLEAN DEFAULT FALSE
);

-- Product Master Table
CREATE TABLE products (
    product_id    INT PRIMARY KEY,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50) NOT NULL,
    brand         VARCHAR(50) NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    stock_qty     INT NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

-- Orders Table
CREATE TABLE orders (
    order_id      INT PRIMARY KEY,
    customer_id   INT NOT NULL,
    order_date    DATE NOT NULL,
    status        VARCHAR(20) NOT NULL DEFAULT 'Pending'
                  CHECK (status IN ('Pending','Shipped','Delivered','Cancelled')),
    total_amount  DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
    item_id       INT PRIMARY KEY,
    order_id      INT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    discount_pct  DECIMAL(5,2) DEFAULT 0 CHECK (discount_pct BETWEEN 0 AND 100),

    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

SHOW TABLES;

-- =====================================================
-- INSERT SAMPLE DATA
-- =====================================================

-- Insert Customers
INSERT INTO customers VALUES (...);

-- Insert Products
INSERT INTO products VALUES (...);

-- Insert Orders
INSERT INTO orders VALUES (...);

-- Insert Order Items
INSERT INTO order_items VALUES (...);

-- =====================================================
-- VIEW TABLE DATA
-- =====================================================

-- Display all customers
SELECT * FROM customers;

-- Display all products
SELECT * FROM products;

-- Display all orders
SELECT * FROM orders;

-- Display all order items
SELECT * FROM order_items;

-- Show customer table structure
DESCRIBE customers;

-- =====================================================
-- BASIC FILTERING QUERIES
-- =====================================================

-- Find electronics products costing more than ₹2000
SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;

-- Find customers from Maharashtra who joined in 2024
SELECT *
FROM customers
WHERE YEAR(join_date) = 2024
AND state = 'Maharashtra';

-- Display customer names and city
SELECT first_name, last_name, city
FROM customers;

-- Display unique product categories
SELECT DISTINCT category
FROM products;

-- =====================================================
-- DATA VALIDATION TEST
-- =====================================================

-- Attempt to insert a product with invalid negative price
INSERT INTO products
(product_id, product_name, category, brand, unit_price, stock_qty)
VALUES
(209, 'Hanging clock', 'Electronics', 'Ajanta', '-50', 200);

-- =====================================================
-- ORDER FILTERING QUERIES
-- =====================================================

-- Show all delivered orders
SELECT *
FROM orders
WHERE status = 'Delivered';

-- Orders between two dates excluding cancelled orders
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status <> 'Cancelled';

-- Customers who joined during 2024
SELECT *
FROM customers
WHERE join_date >= '2024-01-01'
AND join_date < '2025-01-01';

-- =====================================================
-- AGGREGATE FUNCTIONS
-- =====================================================

-- Total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Total revenue from delivered orders
SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE status = 'Delivered';

-- Average product price by category
SELECT category,
       AVG(unit_price) AS avg_unit_price
FROM products
GROUP BY category;

-- Orders and revenue grouped by status
SELECT status,
       COUNT(*) AS order_count,
       SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Most expensive and cheapest product in each category
SELECT category,
       MAX(unit_price) AS most_expensive,
       MIN(unit_price) AS cheapest
FROM products
GROUP BY category;

-- Categories with average price greater than ₹2000
SELECT category,
       AVG(unit_price) AS avg_unit_price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;

-- =====================================================
-- JOINS
-- =====================================================

-- Orders with customer details
SELECT o.order_id,
       o.order_date,
       c.first_name,
       c.last_name,
       o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;

-- All customers and their orders
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       o.order_id,
       o.order_date,
       o.status,
       o.total_amount
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

-- Order details with product information
SELECT o.order_id,
       p.product_name,
       oi.quantity,
       oi.unit_price,
       oi.discount_pct
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id;

-- =====================================================
-- CASE STATEMENT QUERIES
-- =====================================================

-- Categorize products into price tiers
SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price < 1000 THEN 'Budget'
           WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
           ELSE 'Premium'
       END AS price_tier
FROM products;

-- Count delivered vs non-delivered orders
SELECT
    SUM(CASE
            WHEN status = 'Delivered' THEN 1
            ELSE 0
        END) AS delivered_orders,

    SUM(CASE
            WHEN status <> 'Delivered' THEN 1
            ELSE 0
        END) AS not_delivered_orders
FROM orders;

-- =====================================================
-- BUSINESS SCENARIO:
-- CREATE NEW ORDER AND UPDATE INVENTORY
-- =====================================================

-- Create a new order
INSERT INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES
(1011, 102, CURDATE(), 'Pending', 1598.00);

-- Add first product to order
INSERT INTO order_items
(item_id, order_id, product_id, quantity, unit_price, discount_pct)
VALUES
(5016, 1011, 206, 1, 1299.00, 0);

-- Add second product to order
INSERT INTO order_items
(item_id, order_id, product_id, quantity, unit_price, discount_pct)
VALUES
(5017, 1011, 208, 1, 599.00, 0);

-- Reduce stock for Bedsheet Set
UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 206;

-- Reduce stock for Cushion Covers
UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 208;

-- Save transaction
COMMIT;

-- Verify inserted order items
SELECT *
FROM order_items;