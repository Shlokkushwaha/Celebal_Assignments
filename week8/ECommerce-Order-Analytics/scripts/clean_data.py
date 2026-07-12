import pandas as pd
import os
import re

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned")

os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

# ==========================================================
# Load CSV Files
# ==========================================================

def load_data():

    customers = pd.read_csv(
        os.path.join(RAW_DATA_PATH, "customers.csv")
    )

    products = pd.read_csv(
        os.path.join(RAW_DATA_PATH, "products.csv")
    )

    orders = pd.read_csv(
        os.path.join(RAW_DATA_PATH, "orders.csv")
    )

    order_items = pd.read_csv(
        os.path.join(RAW_DATA_PATH, "order_items.csv")
    )

    print("All CSV files loaded successfully.")

    return customers, products, orders, order_items

# ==========================================================
# Customer Cleaning
# ==========================================================

def clean_customers(customers):

    print("\nCleaning Customers...")

    customers["customer_name"] = (
        customers["customer_name"]
        .str.strip()
    )

    customers["registration_date"] = pd.to_datetime(
        customers["registration_date"],
        errors="coerce"
    )

    return customers

# ==========================================================
# Email Validation
# ==========================================================

def validate_emails(customers):

    print("\nValidating Emails...")

    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    customers["email_valid"] = customers["email"].str.match(
        email_pattern,
        na=False
    )

    invalid_emails = (~customers["email_valid"]).sum()

    print(f"Invalid Emails : {invalid_emails}")

    return customers


# ==========================================================
# Product Cleaning
# ==========================================================

def clean_products(products):

    print("\nCleaning Products...")

    # Remove leading/trailing spaces
    products["product_name"] = (
        products["product_name"]
        .str.strip()
        .str.title()
    )

    # Remove duplicate products
    before = len(products)

    products = products.drop_duplicates(
        subset="product_id"
    )

    after = len(products)

    print(f"Duplicate Products Removed : {before-after}")

    return products


# ==========================================================
# Orders Cleaning
# ==========================================================

def clean_orders(orders):

    print("\nCleaning Orders...")

    # Handle mixed date formats
    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        format="mixed",
        errors="coerce"
    )

    invalid_dates = orders["order_date"].isna().sum()

    missing_customer = orders["customer_id"].isna().sum()

    print(f"Invalid Order Dates : {invalid_dates}")

    print(f"Missing Customer IDs : {missing_customer}")

    return orders


# ==========================================================
# Order Items Cleaning
# ==========================================================

def clean_order_items(order_items):

    print("\nCleaning Order Items...")

    # Returns
    order_items["is_return"] = (
        order_items["quantity"] < 0
    )

    total_returns = order_items["is_return"].sum()

    # Convert negative quantity to positive
    order_items["quantity"] = (
        order_items["quantity"]
        .abs()
    )

    # Remove impossible discounts
    order_items.loc[
        order_items["discount_percent"] > 100,
        "discount_percent"
    ] = 100

    order_items.loc[
        order_items["discount_percent"] < 0,
        "discount_percent"
    ] = 0

    print(f"Returned Items : {total_returns}")

    return order_items

# ==========================================================
# Referential Integrity Check
# ==========================================================

def check_referential_integrity(customers, products, orders, order_items):

    print("\nChecking Referential Integrity...")

    invalid_customers = orders[
        (~orders["customer_id"].isin(customers["customer_id"])) &
        (orders["customer_id"].notna())
    ]

    invalid_products = order_items[
        ~order_items["product_id"].isin(products["product_id"])
    ]

    invalid_orders = order_items[
        ~order_items["order_id"].isin(orders["order_id"])
    ]

    print(f"Invalid Customer References : {len(invalid_customers)}")
    print(f"Invalid Product References  : {len(invalid_products)}")
    print(f"Invalid Order References    : {len(invalid_orders)}")

    return (
        invalid_customers,
        invalid_products,
        invalid_orders
    )


# ==========================================================
# Validation Report
# ==========================================================

def generate_validation_report(
    customers,
    orders,
    order_items,
    invalid_customers,
    invalid_products,
    invalid_orders
):

    report = pd.DataFrame({

        "Issue":[
            "Invalid Emails",
            "Invalid Registration Dates",
            "Missing Customer IDs",
            "Returned Orders",
            "Invalid Customer References",
            "Invalid Product References",
            "Invalid Order References"
        ],

        "Count":[
            (~customers["email_valid"]).sum(),
            customers["registration_date"].isna().sum(),
            orders["customer_id"].isna().sum(),
            order_items["is_return"].sum(),
            len(invalid_customers),
            len(invalid_products),
            len(invalid_orders)
        ]

    })

    report.to_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "validation_report.csv"
        ),
        index=False
    )

    print("\nValidation Report Generated Successfully.")


# ==========================================================
# Save Cleaned Files
# ==========================================================

def save_cleaned_files(
    customers,
    products,
    orders,
    order_items
):

    customers.to_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "customers_cleaned.csv"
        ),
        index=False
    )

    products.to_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "products_cleaned.csv"
        ),
        index=False
    )

    orders.to_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "orders_cleaned.csv"
        ),
        index=False
    )

    order_items.to_csv(
        os.path.join(
            CLEANED_DATA_PATH,
            "order_items_cleaned.csv"
        ),
        index=False
    )

    print("\nCleaned CSV files saved successfully.")


# ==========================================================
# Main Function
# ==========================================================

def main():

    customers, products, orders, order_items = load_data()

    customers = clean_customers(customers)

    customers = validate_emails(customers)

    products = clean_products(products)

    orders = clean_orders(orders)

    order_items = clean_order_items(order_items)

    (
        invalid_customers,
        invalid_products,
        invalid_orders
    ) = check_referential_integrity(
        customers,
        products,
        orders,
        order_items
    )

    generate_validation_report(
        customers,
        orders,
        order_items,
        invalid_customers,
        invalid_products,
        invalid_orders
    )

    save_cleaned_files(
        customers,
        products,
        orders,
        order_items
    )

    print("\n" + "=" * 60)
    print("CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"Customers    : {len(customers)}")
    print(f"Products     : {len(products)}")
    print(f"Orders       : {len(orders)}")
    print(f"Order Items  : {len(order_items)}")

    print("\nCleaned files saved in:")
    print(CLEANED_DATA_PATH)


if __name__ == "__main__":
    main()