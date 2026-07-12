import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "ecommerce.db"
)

conn = sqlite3.connect(DB_PATH)

def menu():

    print("\n" + "="*60)
    print("        E-Commerce Analytics Dashboard")
    print("="*60)

    print(" 1. Total Customers")
    print(" 2. Total Products")
    print(" 3. Total Orders")
    print(" 4. Total Revenue")
    print(" 5. Top 10 Selling Products")
    print(" 6. Revenue by Category")
    print(" 7. Orders by Status")
    print(" 8. Customers by Type")
    print(" 9. Top 10 Customers by Spending")
    print("10. Orders by Region")
    print("11. Average Order Value")
    print("12. Returned Items")
    print("13. Most Expensive Products")
    print("14. Average Discount")
    print("15. Customer Registration by Year")
    print("16. Highest Revenue Region")
    print("17. Average Discount per Category")
    print("18. Exit")

def execute_query(query):

    df = pd.read_sql_query(query, conn)

    print("\n")

    print(df)

    print("\nRows Returned :", len(df))


while True:

    menu()

    choice = input("\nEnter Choice : ")

    if choice == "1":

        execute_query("""
        SELECT COUNT(*) AS Total_Customers
        FROM customers;
        """)

    elif choice == "2":

        execute_query("""
        SELECT COUNT(*) AS Total_Products
        FROM products;
        """)

    elif choice == "3":

        execute_query("""
        SELECT COUNT(*) AS Total_Orders
        FROM orders;
        """)

    elif choice == "4":

        execute_query("""
        SELECT
        ROUND(
        SUM(
        quantity *
        unit_price *
        (1-discount_percent/100.0)
        ),2)
        AS Total_Revenue
        FROM order_items;
        """)

    elif choice == "5":

        execute_query("""
        SELECT
        p.product_name,
        SUM(oi.quantity) AS Total_Quantity

        FROM order_items oi

        JOIN products p

        ON oi.product_id = p.product_id

        GROUP BY p.product_name

        ORDER BY Total_Quantity DESC

        LIMIT 10;
        """)

    elif choice == "6":

        execute_query("""
        SELECT

        p.category,

        ROUND(
        SUM(
        oi.quantity *
        oi.unit_price *
        (1-oi.discount_percent/100.0)
        ),2) AS Revenue

        FROM order_items oi

        JOIN products p

        ON oi.product_id = p.product_id

        GROUP BY p.category

        ORDER BY Revenue DESC;
        """)

    elif choice == "7":

        execute_query("""
        SELECT
        status,
        COUNT(*) AS Total_Orders

        FROM orders

        GROUP BY status;
        """)

    elif choice == "8":

        execute_query("""
        SELECT
        customer_type,
        COUNT(*) AS Total_Customers

        FROM customers

        GROUP BY customer_type;
        """)

    elif choice == "9":

        execute_query("""
        SELECT

        c.customer_name,

        ROUND(
        SUM(
        oi.quantity *
        oi.unit_price *
        (1-oi.discount_percent/100.0)
        ),2) AS Spending

        FROM customers c

        JOIN orders o
        ON c.customer_id = o.customer_id

        JOIN order_items oi
        ON o.order_id = oi.order_id

        GROUP BY c.customer_name

        ORDER BY Spending DESC

        LIMIT 10;
        """)

    elif choice == "10":

        execute_query("""
        SELECT
        region_code,
        COUNT(*) AS Total_Orders

        FROM orders

        GROUP BY region_code;
        """)

    elif choice == "11":

        execute_query("""
        SELECT

        ROUND(
        AVG(order_total),2
        ) AS Average_Order_Value

        FROM(

        SELECT

        order_id,

        SUM(
        quantity *
        unit_price *
        (1-discount_percent/100.0)
        ) AS order_total

        FROM order_items

        GROUP BY order_id

        );
        """)

    elif choice == "12":

        execute_query("""
        SELECT
        COUNT(*) AS Returned_Items
        FROM order_items
        WHERE is_return = 1;
        """)

    elif choice == "13":

        execute_query("""
        SELECT
        product_name,
        cost_price

        FROM products

        ORDER BY cost_price DESC

        LIMIT 10;
        """)

    elif choice == "14":

        execute_query("""
        SELECT
        ROUND(
        AVG(discount_percent),2
        ) AS Average_Discount

        FROM order_items;
        """)

    elif choice == "15":

        execute_query("""
        SELECT

        strftime('%Y', registration_date) AS Registration_Year,

        COUNT(*) AS Total_Customers

        FROM customers

        GROUP BY Registration_Year;
        """)

    elif choice == "16":

        execute_query("""
        SELECT

        o.region_code,

        ROUND(
        SUM(
        oi.quantity *
        oi.unit_price *
        (1-oi.discount_percent/100.0)
        ),2) AS Revenue

        FROM orders o

        JOIN order_items oi

        ON o.order_id = oi.order_id

        GROUP BY o.region_code

        ORDER BY Revenue DESC;
        """)

    elif choice == "17":

        execute_query("""
        SELECT

        p.category,

        ROUND(
        AVG(oi.discount_percent),2
        ) AS Average_Discount

        FROM order_items oi

        JOIN products p

        ON oi.product_id = p.product_id

        GROUP BY p.category;
        """)

    elif choice == "18":

        conn.close()

        print("\nThank You!")

        break

    else:

        print("\nInvalid Choice. Please enter a number between 1 and 18.")