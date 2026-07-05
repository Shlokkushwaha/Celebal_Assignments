# Data Engineering Assignment 003

## Superstore Sales Analysis using SQL

### Objective

The objective of this assignment is to analyze sales data from the Superstore dataset using advanced SQL concepts such as:

* Subqueries
* Common Table Expressions (CTEs)
* Window Functions
* Joins
* Aggregations

---

## Dataset

The Superstore dataset was imported into a raw table named:

```sql
superstore_raw
```

The following tables were created using `SELECT DISTINCT`:

* `customers`
* `products`
* `orders`

---

## Database Schema

### Customers Table

Contains unique customer information:

* Customer ID
* Customer Name
* Segment

### Products Table

Contains unique product information:

* Product ID
* Product Name
* Category
* Sub Category

### Orders Table

Contains transactional sales data:

* Order ID
* Order Date
* Ship Date
* Customer ID
* Product ID
* Sales
* Quantity
* Profit

---

## SQL Concepts Implemented

### Subqueries

1. Orders with sales greater than average sales.
2. Highest sales order for each customer.

### Common Table Expressions (CTEs)

1. Total sales per customer.
2. Customers whose total sales are above average.

### Window Functions

1. `ROW_NUMBER()`
2. `RANK()`

### Combined SQL Concepts

A final query was created using:

* JOIN
* CTE
* Window Function

to display customer sales rankings.

---

## Business Questions Solved

### 1. Top Customers by Sales

Identified customers contributing the highest revenue.

### 2. Bottom Customers by Sales

Identified customers with the lowest revenue contribution.

### 3. Single Order Customers

Found customers who placed only one order.

### 4. Above Average Customers

Identified customers whose total sales exceed the average customer sales.

### 5. Highest Order Value per Customer

Determined the highest sales order for every customer.

### 6. Top 3 Customers

Ranked customers based on total sales and displayed the top performers.

---

## Screenshots Included

1. Dataset Import Verification
2. Customers Table Creation
3. Products Table Creation
4. Orders Table Creation
5. Orders Above Average Sales
6. Highest Sales Order Per Customer
7. Total Sales Per Customer (CTE)
8. Above Average Customers (CTE)
9. ROW_NUMBER() Window Function
10. Customer Ranking using RANK()
11. Top 3 Customers
12. Top 5 Customers
13. Bottom 5 Customers
14. Single Order Customers
15. Final Combined Query

---

## Key Insights

1. A small group of customers contributes a significant portion of total sales.
2. Several customers placed only one order, indicating low engagement.
3. Multiple customers generated sales above the average customer spending.
4. Window functions provide an efficient way to rank customers based on revenue.
5. CTEs simplify complex analytical queries and improve readability.
6. Customer ranking helps identify high-value customers for targeted business strategies.

---
assignment_03 -> contains all the queries
data-> Sample_superstore.csv
Screenshots

## Technologies Used

* MySQL
* MySQL Workbench
* SQL



---

## Conclusion

This project demonstrates the use of SQL for data analysis and business intelligence. By applying subqueries, CTEs, window functions, and joins, meaningful insights were extracted from the Superstore sales dataset to support decision-making and customer analysis.
