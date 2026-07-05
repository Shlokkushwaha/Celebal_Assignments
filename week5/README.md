# Apache Spark Data Cleaning and Transformation Assignment

## 📌 Objective

This assignment demonstrates the use of Apache Spark DataFrames for data cleaning, transformation, filtering, aggregation, and schema modification operations. The goal is to understand Spark fundamentals and perform common data engineering tasks using PySpark.

---

## 🛠 Technologies Used

- Apache Spark
- PySpark
- Databricks
- CSV Dataset
- GitHub

---

## 📂 Project Structure

```
├── spark_assignment_dataset.csv
├── Spark_Assignment.ipynb
├── README.md
```

---

## 📊 Dataset Overview

A custom dataset was created containing the following columns:

- user_id
- transaction_date
- region
- product_category
- sale_amount
- status
- city
- age
- subscription
- raw_timestamp
- email
- username
- price
- store_id

The dataset includes:

- Duplicate records
- Null values
- Empty strings
- Multiple regions and categories
- Timestamp data

These characteristics allow all assignment operations to be performed.

---

## 📖 Assignment Questions Covered

### Q1. Limitations of MapReduce
- Explained why Spark is preferred over traditional MapReduce.

### Q2. In-Memory Computing
- Explained Spark's in-memory processing and performance benefits.

### Q3. Remove Duplicate Rows
- Used `dropDuplicates()` on `user_id` and `transaction_date`.

### Q4. Filter and Aggregate Data
- Filtered West region records.
- Calculated average sales by product category.

### Q5. Handle Null Values
- Demonstrated `.na.drop()`
- Demonstrated `.na.fill()`

### Q6. Count Records by City
- Used `groupBy()` and `count()`.

### Q7. DataFrame Immutability
- Explained immutable nature of Spark DataFrames.

### Q8. Conditional Filtering
- Filtered users aged 18–30 with Premium subscriptions.

### Q9. Importance of Handling Nulls
- Explained impact on aggregations.

### Q10. Timestamp Conversion
- Cast string timestamp to `TimestampType`.

### Q11. Shuffle and Wide Transformations
- Explained Spark shuffle process.

### Q12. Data Cleaning
- Removed rows with null emails or empty usernames.

### Q13. Multiple Aggregations
- Calculated Min, Max, and Mean price.

### Q14. Risks of inferSchema
- Explained schema inference challenges.

### Q15. End-to-End Processing Pipeline
- Removed duplicates
- Filled null prices
- Aggregated revenue by store

---

## 🚀 Sample Spark Operations

### Remove Duplicates

```python
df.dropDuplicates(["user_id", "transaction_date"])
```

### Fill Null Values

```python
df.na.fill({"status": "Unknown"})
```

### Group By and Aggregation

```python
df.groupBy("store_id") \
  .agg(sum("price").alias("total_revenue"))
```

---

## 📈 Key Insights

- Duplicate records were successfully removed.
- Missing values were handled using Spark DataFrame functions.
- Filtering operations reduced unnecessary records.
- Aggregations provided meaningful business insights.
- Spark's DataFrame API simplified data transformation workflows.

---

## 🎯 Learning Outcomes

After completing this assignment, I learned:

- Spark DataFrame operations
- Data cleaning techniques
- Aggregation and grouping
- Filtering datasets
- Handling null values
- Schema modifications
- Spark transformations and actions
- Wide vs Narrow transformations
- End-to-end data processing pipelines

---

## 👨‍💻 Author

**Shlok Kushwaha**

B.Tech CSE Student | Aspiring Data Engineer
