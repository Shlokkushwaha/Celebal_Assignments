# 🛒 Enterprise E-Commerce Order Analytics Pipeline

An end-to-end Data Engineering project that simulates a real-world E-Commerce analytics pipeline. The project generates synthetic transactional data, performs data cleaning and validation using Pandas, loads the processed data into SQLite, and provides business insights through SQL queries and an interactive analytics dashboard.

---

## 📌 Project Objective

The objective of this project is to build a complete ETL (Extract, Transform, Load) pipeline using Python, Pandas, SQLite, and SQL. The project demonstrates how raw business data can be transformed into meaningful insights through data engineering workflows.

---

## 🚀 Features

- Generate realistic E-Commerce datasets using Faker
- Introduce real-world dirty data
- Perform data cleaning and validation
- Validate referential integrity between tables
- Load cleaned data into SQLite database
- Execute business analytics using SQL
- Interactive menu-driven analytics dashboard
- Validation report generation

---

## 🏗️ Project Architecture

```
                +----------------------+
                |  generate_data.py    |
                +----------+-----------+
                           |
                           v
               Raw CSV Files Generated
                           |
                           v
                +----------------------+
                |   clean_data.py      |
                +----------+-----------+
                           |
                           v
             Cleaned & Validated CSV Files
                           |
                           v
               +-----------------------+
               | load_database.py      |
               +----------+------------+
                           |
                           v
                   SQLite Database
                           |
                           v
                +----------------------+
                |    dashboard.py      |
                +----------+-----------+
                           |
                           v
                 Business Analytics Reports
```

---

# 📂 Project Structure

```
ECommerce-Order-Analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
│   └── ecommerce.db
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   └── dashboard.py
│
├── sql/
│   └── queries.sql
│
├── reports/
│   └── validation_report.csv
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Faker
- VS Code

---

# 📊 Dataset Overview

The project generates four datasets.

## Customers

| Column |
|---------|
| customer_id |
| customer_name |
| email |
| registration_date |
| customer_type |

Records: **1000**

---

## Products

| Column |
|---------|
| product_id |
| product_name |
| category |
| subcategory |
| cost_price |

Records: **300**

---

## Orders

| Column |
|---------|
| order_id |
| customer_id |
| order_date |
| status |
| region_code |

Records: **1000**

---

## Order Items

| Column |
|---------|
| item_id |
| order_id |
| product_id |
| quantity |
| unit_price |
| discount_percent |

Records: **3000**

---

# 🧹 Data Cleaning Performed

The pipeline performs the following data quality checks:

- Remove leading and trailing spaces
- Validate email addresses using Regex
- Standardize product names
- Convert mixed date formats
- Detect missing customer IDs
- Handle returned items using negative quantities
- Create `is_return` flag
- Validate referential integrity
- Generate validation report

---

# 📈 SQL Reports

The dashboard supports the following business reports:

1. Total Customers
2. Total Products
3. Total Orders
4. Total Revenue
5. Top 10 Selling Products
6. Revenue by Category
7. Orders by Status
8. Customers by Type
9. Top 10 Customers by Spending
10. Orders by Region
11. Average Order Value
12. Returned Items
13. Most Expensive Products
14. Average Discount
15. Customer Registration by Year
16. Highest Revenue Region
17. Average Discount per Category

---

# ▶️ How to Run

## Clone Repository

```bash
git clone https://github.com/your-username/ECommerce-Order-Analytics.git

cd ECommerce-Order-Analytics
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Generate Dataset

```bash
python scripts/generate_data.py
```

---

## Clean Dataset

```bash
python scripts/clean_data.py
```

---

## Load SQLite Database

```bash
python scripts/load_database.py
```

---

## Launch Analytics Dashboard

```bash
python scripts/report.py
```

---

# 📊 Sample Dashboard

```
====================================================
        E-Commerce Analytics Dashboard
====================================================

1. Total Customers
2. Total Products
3. Total Orders
4. Total Revenue
5. Top Selling Products
...
17. Average Discount per Category
18. Exit
```

---

# 📚 Concepts Demonstrated

- ETL Pipeline
- Data Engineering Workflow
- Data Cleaning
- Data Validation
- Referential Integrity
- Relational Database Design
- SQL Analytics
- Aggregate Functions
- JOIN Operations
- GROUP BY
- Data Quality Checks
- Interactive Reporting

---

# 🎯 Learning Outcomes

Through this project I learned how to:

- Design a complete ETL pipeline
- Generate realistic datasets
- Handle dirty data
- Clean and validate datasets using Pandas
- Store processed data in SQLite
- Write business-focused SQL queries
- Build an interactive reporting system
- Apply data engineering best practices

---

# 📌 Future Enhancements

- Replace SQLite with PostgreSQL
- Build interactive dashboards using Power BI or Tableau
- Automate pipeline scheduling using Apache Airflow
- Migrate processing to PySpark
- Store data in Delta Lake
- Deploy pipeline on Databricks or Azure

---

# 👨‍💻 Author

**Shlok Kushwaha**

B.Tech Computer Science Engineering

Data Engineering Intern @ Celebal Technologies

GitHub: https://github.com/Shlokkushwaha

LinkedIn: https://www.linkedin.com/in/shlok-kushwaha/