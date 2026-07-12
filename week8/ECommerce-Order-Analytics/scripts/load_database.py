import sqlite3
import pandas as pd
import os

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLEANED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database"
)

os.makedirs(DATABASE_PATH, exist_ok=True)

DB_FILE = os.path.join(
    DATABASE_PATH,
    "ecommerce.db"
)

# ==========================================================
# Load Cleaned CSV Files
# ==========================================================

def load_cleaned_data():

    customers = pd.read_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "customers_cleaned.csv"
        )
    )

    products = pd.read_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "products_cleaned.csv"
        )
    )

    orders = pd.read_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "orders_cleaned.csv"
        )
    )

    order_items = pd.read_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "order_items_cleaned.csv"
        )
    )

    print("Cleaned CSV files loaded successfully.")

    return customers, products, orders, order_items

# ==========================================================
# Create SQLite Database
# ==========================================================

def create_database():

    conn = sqlite3.connect(DB_FILE)

    print("SQLite Database Connected.")

    return conn

# ==========================================================
# Load Tables into SQLite
# ==========================================================

def load_tables(
    conn,
    customers,
    products,
    orders,
    order_items
):

    customers.to_sql(
        "customers",
        conn,
        if_exists="replace",
        index=False
    )

    products.to_sql(
        "products",
        conn,
        if_exists="replace",
        index=False
    )

    orders.to_sql(
        "orders",
        conn,
        if_exists="replace",
        index=False
    )

    order_items.to_sql(
        "order_items",
        conn,
        if_exists="replace",
        index=False
    )

    print("\nTables Loaded Successfully.")
    
    
# ==========================================================
# Verify Tables
# ==========================================================

def verify_tables(conn):

    cursor = conn.cursor()

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    print("\nDatabase Summary")

    print("=" * 40)

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{table:<15} {count}")

    print("=" * 40)
    

# ==========================================================
# Main
# ==========================================================

def main():

    customers, products, orders, order_items = load_cleaned_data()

    conn = create_database()

    load_tables(
        conn,
        customers,
        products,
        orders,
        order_items
    )

    verify_tables(conn)

    conn.close()

    print("\nDatabase Connection Closed.")

    print("\nSUCCESS : ecommerce.db Created")


if __name__ == "__main__":
    main()