CREATE DATABASE superstore_db;
use superstore_db;

SHOW TABLES;

SELECT * 
FROM superstore
LIMIT 10;

-- exploring schema
DESCRIBE superstore;

SELECT COUNT(*)
FROM superstore;

-- Basic Filtering Queries
SELECT sales
FROM superstore
WHERE region = 'south';

SELECT *
FROM superstore
WHERE CAtegory = 'technology';

SELECT *
FROM superstore
WHERE sales > 500;

-- Aggregation Queries
-- Total Sales
SELECT SUM(sales) AS total_sales
FROM superstore;

-- Total Quantity Sold
SELECT SUM(quantity) AS total_quantity
FROM superstore;

-- Average Profit
SELECT AVG(profit), `ship mode`
FROM superstore
GROUP BY `ship mode`;

-- GROUP BY Queries
-- Sales by Region
SELECT region, SUM(sales) AS total_sales
FROM superstore
GROUP BY region;

-- Profit by Category
SELECT category, SUM(profit) AS total_profit
FROM superstore
GROUP BY category;

-- Top Customers by Sales
SELECT `customer name`, SUM(sales)
FROM superstore
GROUP BY `customer name`
ORDER BY SUM(sales) DESC
LIMIT 10;

SELECT category, sum(sales) AS total_sum
FROM superstore
GROUP BY category
ORDER BY total_sum DESC;

-- Sorting & Limiting
SELECT *
FROM superstore
ORDER BY Sales DESC
LIMIT 5;

-- USE CASES
-- Monthly Sales Trend
SELECT MONTH(`order date`) AS month, SUM(sales)
FROM superstore
GROUP BY MONTH(`ORDER DATE`)
ORDER BY month;

-- Top Selling Products
SELECT `product name`, SUM(quantity) AS total_quantity
FROM superstore
GROUP BY `product name` 
ORDER BY total_quantity DESC
LIMIT 10;

-- Most Profitable Category
SELECT category, SUM(profit) AS total_profit
FROM superstore
GROUP BY category
ORDER BY total_profit DESC;

-- Duplicate Check
SELECT `ORDER ID`, COUNT(`ORDER ID`) AS count
FROM superstore
GROUP BY `ORDER ID`
HAVING COUNT(`ORDER ID`) > 1;

-- Null Value Check
SELECT COUNT(*)
FROM superstore
WHERE profit IS NULL;

-- Data Validation
SELECT COUNT(*) FROM superstore;

-- Distinct Categories
SELECT DISTINCT category
FROM superstore;
