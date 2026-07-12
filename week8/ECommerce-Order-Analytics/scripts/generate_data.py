import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(RAW_DATA_PATH, exist_ok=True)

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 300
NUM_ORDERS = 1000
NUM_ORDER_ITEMS = 3000

CATEGORIES = {
    "Electronics": [
        "Mobile",
        "Laptop",
        "Tablet",
        "Camera",
        "Headphones"
    ],
    "Clothing": [
        "Shirt",
        "T-Shirt",
        "Jeans",
        "Shoes",
        "Jacket"
    ],
    "Books": [
        "Programming",
        "History",
        "Science",
        "Novel",
        "Biography"
    ],
    "Home": [
        "Kitchen",
        "Furniture",
        "Decor",
        "Lighting",
        "Storage"
    ]
}

ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

REGIONS = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]

PRODUCT_BRANDS = {

    "Mobile": [
        "Samsung Galaxy S24",
        "iPhone 16",
        "OnePlus 13",
        "Google Pixel 9",
        "Xiaomi 15"
    ],

    "Laptop": [
        "Dell Inspiron",
        "HP Pavilion",
        "MacBook Air M3",
        "Lenovo ThinkPad",
        "ASUS Vivobook"
    ],

    "Tablet": [
        "iPad Air",
        "Samsung Tab S10",
        "OnePlus Pad",
        "Lenovo Tab"
    ],

    "Camera": [
        "Canon EOS",
        "Sony Alpha",
        "Nikon D750",
        "GoPro Hero"
    ],

    "Headphones": [
        "Sony WH1000XM5",
        "AirPods Pro",
        "Boat Rockerz",
        "JBL Tune"
    ],

    "Shirt": [
        "Formal Shirt",
        "Casual Shirt",
        "Linen Shirt"
    ],

    "T-Shirt": [
        "Graphic Tee",
        "Polo T-Shirt",
        "Round Neck Tee"
    ],

    "Jeans": [
        "Slim Fit Jeans",
        "Regular Jeans",
        "Cargo Jeans"
    ],

    "Shoes": [
        "Nike Air Max",
        "Adidas Run",
        "Puma Sneakers"
    ],

    "Jacket": [
        "Leather Jacket",
        "Bomber Jacket",
        "Winter Jacket"
    ],

    "Programming": [
        "Python Crash Course",
        "Clean Code",
        "System Design"
    ],

    "History": [
        "World History",
        "Indian History"
    ],

    "Science": [
        "Physics Basics",
        "Astronomy"
    ],

    "Novel": [
        "The Alchemist",
        "Harry Potter"
    ],

    "Biography": [
        "Steve Jobs",
        "APJ Abdul Kalam"
    ],

    "Kitchen": [
        "Mixer Grinder",
        "Pressure Cooker"
    ],

    "Furniture": [
        "Office Chair",
        "Study Table"
    ],

    "Decor": [
        "Wall Clock",
        "Flower Vase"
    ],

    "Lighting": [
        "LED Lamp",
        "Ceiling Light"
    ],

    "Storage": [
        "Plastic Box",
        "Bookshelf"
    ]
}

def generate_customers():

    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):

        # Generate email
        email = fake.email()

        # Make 2% emails invalid
        if random.random() < 0.02:

            invalid_type = random.choice([
                "missing_at",
                "missing_domain"
            ])

            if invalid_type == "missing_at":
                email = email.replace("@", "")

            else:
                email = email.split("@")[0] + "@"

        customer = {

            "customer_id": f"C{i:04d}",

            "customer_name": fake.name(),

            "email": email,

            "registration_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            ),

            "customer_type": random.choice(CUSTOMER_TYPES)

        }

        customers.append(customer)

    df = pd.DataFrame(customers)

    df.to_csv(
        os.path.join(RAW_DATA_PATH, "customers.csv"),
        index=False
    )

    print("\n✅ customers.csv generated successfully!")
    print(f"Total Customers: {len(df)}")
    print("\nFirst 5 Customers:")
    print(df.head())

    return df


def generate_products():

    products = []

    for i in range(1, NUM_PRODUCTS + 1):

        product_id = f"P{i:04d}"

        # Random Category
        category = random.choice(list(CATEGORIES.keys()))

        # Random Subcategory
        subcategory = random.choice(CATEGORIES[category])

        # Random Product Name
        product_name = random.choice(PRODUCT_BRANDS[subcategory])

        # Add dirty data (5%)
        if random.random() < 0.05:

            style = random.choice([
                "upper",
                "lower",
                "spaces"
            ])

            if style == "upper":
                product_name = product_name.upper()

            elif style == "lower":
                product_name = product_name.lower()

            else:
                product_name = "   " + product_name + "   "

        cost_price = random.randint(100, 100000)

        product = {

            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price

        }

        products.append(product)

    df = pd.DataFrame(products)

    df.to_csv(
        os.path.join(RAW_DATA_PATH, "products.csv"),
        index=False
    )

    print("\n✅ products.csv generated successfully!")
    print(f"Total Products : {len(df)}")
    print(df.head())

    return df

def generate_orders(customers_df):

    orders = []

    customer_ids = customers_df["customer_id"].tolist()

    for i in range(1, NUM_ORDERS + 1):

        order_id = f"O{i:04d}"

        # 5% Missing Customer IDs
        if random.random() < 0.05:
            customer_id = None
        else:
            customer_id = random.choice(customer_ids)

        # Random datetime within last 2 years
        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        # 5% Wrong Date Format
        if random.random() < 0.05:
            order_date = order_date.strftime("%d-%m-%Y %H:%M:%S")
        else:
            order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")

        status = random.choice(ORDER_STATUS)

        region = random.choice(REGIONS)

        order = {

            "order_id": order_id,

            "customer_id": customer_id,

            "order_date": order_date,

            "status": status,

            "region_code": region

        }

        orders.append(order)

    df = pd.DataFrame(orders)

    df.to_csv(
        os.path.join(RAW_DATA_PATH, "orders.csv"),
        index=False
    )

    print("\n✅ orders.csv generated successfully!")
    print(f"Total Orders : {len(df)}")
    print(df.head())

    return df

def generate_order_items(orders_df, products_df):

    order_items = []

    order_ids = orders_df["order_id"].tolist()
    product_ids = products_df["product_id"].tolist()

    # Create a lookup dictionary for product prices
    price_lookup = dict(
        zip(products_df["product_id"], products_df["cost_price"])
    )

    for i in range(1, NUM_ORDER_ITEMS + 1):

        item_id = f"I{i:05d}"

        order_id = random.choice(order_ids)

        product_id = random.choice(product_ids)

        quantity = random.randint(1, 5)

        # 3% negative quantity (Returns)
        if random.random() < 0.03:
            quantity = -quantity

        cost_price = price_lookup[product_id]

        # Selling price (20% to 60% profit)
        unit_price = round(
            cost_price * random.uniform(1.2, 1.6),
            2
        )

        discount_percent = random.randint(0, 50)

        order_item = {

            "item_id": item_id,

            "order_id": order_id,

            "product_id": product_id,

            "quantity": quantity,

            "unit_price": unit_price,

            "discount_percent": discount_percent

        }

        order_items.append(order_item)

    df = pd.DataFrame(order_items)

    df.to_csv(
        os.path.join(RAW_DATA_PATH, "order_items.csv"),
        index=False
    )

    print("\n✅ order_items.csv generated successfully!")
    print(f"Total Order Items : {len(df)}")
    print(df.head())

    return df

if __name__ == "__main__":

    print("=" * 60)
    print("Generating Customers...")
    customers_df = generate_customers()

    print("=" * 60)
    print("Generating Products...")
    products_df = generate_products()

    print("=" * 60)
    print("Generating Orders...")
    orders_df = generate_orders(customers_df)

    print("=" * 60)
    print("Generating Order Items...")
    order_items_df = generate_order_items(
        orders_df,
        products_df
    )

    print("=" * 60)
    print("🎉 ALL CSV FILES GENERATED SUCCESSFULLY!")