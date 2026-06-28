"""
Week 6 - Spark Assignment
=========================
Topics: Spark Architecture, Lazy Evaluation, DAG, Transformations & Actions,
        CSV vs Parquet, Schema Handling, Filtering, Predicate Pushdown,
        Client Mode vs Cluster Mode
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import DoubleType

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Week6_Spark_Assignment") \
    .getOrCreate()

# ─────────────────────────────────────────────────────────────────────────────
# Q1: Explain the roles of Driver, Cluster Manager, and Executor
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

Driver:
    The Driver is the master process that runs the main() function of the
    Spark application. It is responsible for:
    - Parsing the user's code and converting it into a logical/physical plan.
    - Building the DAG (Directed Acyclic Graph) of stages and tasks.
    - Coordinating with the Cluster Manager to acquire resources.
    - Distributing tasks to Executors and collecting the final results.

Cluster Manager:
    The Cluster Manager is the resource-allocation layer that sits between
    the Driver and the actual worker nodes. Examples include YARN, Mesos,
    Kubernetes, and Spark's built-in Standalone manager. Its responsibilities:
    - Allocating CPU cores and memory to the Spark application.
    - Launching Executor processes on worker nodes.
    - Monitoring the health of worker nodes.

Executor:
    Executors are JVM processes launched on worker nodes. Each Executor:
    - Runs the tasks assigned to it by the Driver.
    - Stores data partitions in memory or on disk (RDD/DataFrame caching).
    - Returns results or status back to the Driver after task completion.
    - Lives for the entire lifetime of the Spark application.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q2: How does Lazy Evaluation improve performance?
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

Spark does NOT execute transformations (map, filter, select, join, etc.)
the moment they are called. Instead, it records them as nodes in a DAG
(logical plan) and waits until an Action (show, count, collect, write)
is triggered.

Performance benefits of Lazy Evaluation:

1. Query Optimization  – Spark's Catalyst Optimizer analyzes the entire
   DAG before execution and rewrites it for efficiency (e.g., pushing
   filters down close to the data source, eliminating unused columns).

2. Predicate Pushdown  – Because the full pipeline is known upfront, Spark
   can tell the data source (e.g., Parquet) to skip irrelevant row-groups
   before reading, drastically reducing I/O.

3. Stage Fusion        – Consecutive narrow transformations (filter → select
   → withColumn) can be combined into a single stage/task, avoiding
   unnecessary intermediate data materialization.

4. Avoiding Redundant Work – If the user chains multiple filters, Spark
   can merge them into one pass over the data instead of multiple scans.

Example:
    df.filter(...).select(...).filter(...)  ← no computation yet
    df.filter(...).select(...).filter(...).show()  ← NOW Spark executes
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q3: Read a CSV file with header and inferSchema
# ─────────────────────────────────────────────────────────────────────────────

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/source.csv")

df.printSchema()
df.show(5)


# ─────────────────────────────────────────────────────────────────────────────
# Q4: CSV vs Parquet – Storage format and performance impact
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

CSV (Row-based):
    - Stores data row by row: [row1_col1, row1_col2, ...], [row2_col1, ...]
    - Human-readable, easy to inspect with a text editor.
    - To read a single column you must read EVERY column on every row.
    - No built-in compression or statistics; schema must be inferred or
      supplied manually.

Parquet (Columnar):
    - Stores data column by column: all values of col1 together, all of
      col2 together, etc.
    - Binary format – not human-readable, but highly efficient.
    - Reading only 2 out of 100 columns reads ≈ 2% of the file bytes.
    - Stores per-column min/max statistics enabling Predicate Pushdown
      (entire row groups are skipped if the filter value is outside the
      range).
    - Excellent compression because same-type, often similar values are
      stored together (e.g., Snappy, Gzip, Zstd).

Why it matters for performance:
    - Analytical queries typically touch a few columns of a wide table.
      Parquet skips the rest → less I/O, less memory, faster scans.
    - Parquet's row-group statistics let Spark skip irrelevant data before
      even reading it into memory, which is impossible with CSV.
    - File sizes are 5–10× smaller in Parquet vs CSV for the same data,
      reducing network transfer in distributed settings.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q5: Select product_id and price where category = 'Electronics'
# ─────────────────────────────────────────────────────────────────────────────

# Assume df is the DataFrame loaded above (or any DataFrame with these columns)
result_q5 = df.filter(col("category") == "Electronics") \
               .select("product_id", "price")

result_q5.show()


# ─────────────────────────────────────────────────────────────────────────────
# Q6: Rename column and cast price to Double
# ─────────────────────────────────────────────────────────────────────────────

df_revised = df \
    .withColumnRenamed("old_name", "new_name") \
    .withColumn("price", col("price").cast(DoubleType()))

df_revised.printSchema()
df_revised.show(5)


# ─────────────────────────────────────────────────────────────────────────────
# Q7: How does Spark use the DAG (Lineage Graph) for fault tolerance?
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

Every transformation applied to an RDD or DataFrame is recorded as an edge
in the DAG (Directed Acyclic Graph), building a complete "lineage" – a
recipe for how to recompute any partition from the original source data.

Fault Tolerance Flow:
    1. A worker node fails mid-computation, losing some data partitions.
    2. Spark's Driver detects the failure (heartbeat timeout).
    3. The Driver consults the DAG/lineage to find where the lost
       partitions came from and which transformations produced them.
    4. Spark re-schedules only the failed tasks on other available
       Executors, recomputing the lost partitions from their parent
       partitions (or from the original source if needed).
    5. No data is lost and no user intervention is required.

Key insight: Because transformations are deterministic (same input always
produces same output) the lineage is sufficient to fully reconstruct any
lost data. This is cheaper than replication (no extra storage cost) and
is the core of Spark's resilience model.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q8: Filter df_orders for status = 'Completed' AND amount > 1000
# ─────────────────────────────────────────────────────────────────────────────

# Create a sample DataFrame for demonstration
from pyspark.sql import Row

sample_orders = [
    Row(order_id=1, status="Completed", amount=1500.0),
    Row(order_id=2, status="Pending",   amount=2000.0),
    Row(order_id=3, status="Completed", amount=800.0),
    Row(order_id=4, status="Completed", amount=1200.0),
]
df_orders = spark.createDataFrame(sample_orders)

result_q8 = df_orders.filter(
    (col("status") == "Completed") & (col("amount") > 1000)
)
result_q8.show()


# ─────────────────────────────────────────────────────────────────────────────
# Q9: Predicate Pushdown in Parquet
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

What is Predicate Pushdown?
    A query optimization where filter conditions (predicates) are "pushed
    down" as close to the data source as possible — ideally into the file
    reader itself — so that irrelevant data is never loaded into memory.

How it works in Parquet:
    Parquet organizes data into "Row Groups" (chunks of ~128 MB by default).
    For each Row Group, Parquet stores per-column statistics:
        - min value
        - max value
        - null count

    When Spark reads a Parquet file with a filter like
        WHERE amount > 5000
    the Parquet reader checks each Row Group's statistics:
        - If a Row Group has max(amount) = 3000 → entire Row Group skipped.
        - Only Row Groups that *could* contain matching rows are read.

Effect on memory:
    - Fewer Row Groups are read from disk → less I/O.
    - Fewer bytes are decompressed and decoded → less CPU.
    - Less data is loaded into Spark's JVM heap → lower memory pressure,
      fewer GC pauses, and smaller shuffle sizes.

Result: Queries on large Parquet datasets with selective filters can be
orders of magnitude faster than equivalent CSV scans, because CSV has no
statistics and must be read row-by-row in full.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q10: Add final_price column = base_price * 1.18 (18% tax)
# ─────────────────────────────────────────────────────────────────────────────

# Sample DataFrame with base_price
sample_products = [
    Row(product_id=101, base_price=500.0),
    Row(product_id=102, base_price=1200.0),
    Row(product_id=103, base_price=299.99),
]
df_products = spark.createDataFrame(sample_products)

df_with_tax = df_products.withColumn(
    "final_price",
    col("base_price") * lit(1.18)
)

df_with_tax.show()


# ─────────────────────────────────────────────────────────────────────────────
# Q11: Difference between Transformations and Actions
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

Transformations:
    - Operations that define a new DataFrame/RDD from an existing one.
    - They are LAZY – no computation happens when they are called; Spark
      just adds them to the DAG.
    - They return a new DataFrame (immutable).

    Examples:
        1. df.filter(col("price") > 100)   – keeps only rows matching the
                                             condition; nothing runs yet.
        2. df.select("product_id", "price") – projects to a subset of
                                             columns; nothing runs yet.
        (Others: withColumn, join, groupBy, orderBy, distinct, union, ...)

Actions:
    - Operations that TRIGGER execution of the DAG and produce a result
      (either to the driver's memory or to an external storage system).
    - They are EAGER – calling them immediately kicks off computation.

    Examples:
        1. df.count()    – computes and returns the number of rows as an
                          integer in the Driver.
        2. df.show(10)   – executes the pipeline and prints the first 10
                          rows to the console.
        (Others: collect(), write(), take(n), first(), saveAsTextFile(), ...)

Key Rule:
    No data moves until an Action is called.
    Transformations build the *plan*; Actions *execute* it.
"""

# Code illustration
lazy_df = df_products.filter(col("base_price") > 500).select("product_id")  # Transformation – nothing runs
count = lazy_df.count()   # Action – DAG executes NOW
print(f"Products with base_price > 500: {count}")


# ─────────────────────────────────────────────────────────────────────────────
# Q12: Load Parquet, filter null user_id, save as CSV
# ─────────────────────────────────────────────────────────────────────────────

df_parquet = spark.read.parquet("path/to/input")

df_clean = df_parquet.filter(col("user_id").isNotNull())

df_clean.write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv("path/to/output")


# ─────────────────────────────────────────────────────────────────────────────
# Q13: Client Mode vs Cluster Mode
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

Client Mode:
    - The Driver process runs on the SAME machine that submitted the job
      (the "client" machine, e.g., your laptop or edge node).
    - The Driver stays alive only as long as the submitting process is alive;
      killing the terminal kills the application.
    - Logs and output appear directly in the client terminal – convenient
      for debugging and interactive sessions (spark-shell, Jupyter notebooks).
    - The client machine must remain connected to the cluster for the
      entire job duration, which makes it unsuitable for long-running jobs.

    Use when: Interactive development, debugging, short-lived jobs.

Cluster Mode:
    - The Driver process runs INSIDE the cluster on one of the worker/
      master nodes, managed by the Cluster Manager (YARN, Kubernetes, etc.).
    - Once submitted, the client can disconnect; the job continues running
      independently on the cluster.
    - Better for production pipelines and long-running batch jobs since
      there is no dependency on the client machine staying alive.
    - Logs are collected by the cluster and accessible via the cluster's
      web UI or logging system.

    Use when: Production ETL jobs, scheduled pipelines, long-running tasks.

Command comparison:
    # Client Mode (default for spark-submit with local/YARN)
    spark-submit --deploy-mode client  my_job.py

    # Cluster Mode
    spark-submit --deploy-mode cluster my_job.py
"""


# ─────────────────────────────────────────────────────────────────────────────
# Q14: Filter where region = 'North' OR priority = 'High'
# ─────────────────────────────────────────────────────────────────────────────

sample_data = [
    Row(order_id=1, region="North", priority="Low"),
    Row(order_id=2, region="South", priority="High"),
    Row(order_id=3, region="East",  priority="Medium"),
    Row(order_id=4, region="North", priority="High"),
]
df_dataset = spark.createDataFrame(sample_data)

result_q14 = df_dataset.filter(
    (col("region") == "North") | (col("priority") == "High")
)
result_q14.show()


# ─────────────────────────────────────────────────────────────────────────────
# Q15: Why use .show(5) instead of .collect() on a multi-terabyte dataset?
# ─────────────────────────────────────────────────────────────────────────────
"""
ANSWER:

.collect():
    - Pulls ALL rows from ALL partitions across ALL Executors into the
      Driver's memory as a Python list.
    - On a multi-terabyte dataset this means:
        * Terabytes of data transferred over the network to a single node.
        * The Driver JVM (typically 4–16 GB heap) runs out of memory and
          crashes with an OutOfMemoryError.
        * Even if the Driver has enough RAM, the process takes an extremely
          long time and starves other applications sharing the cluster.
    - collect() is only safe on small DataFrames (after heavy aggregation
      or filtering has reduced the data to thousands of rows, not billions).

.show(5):
    - Fetches only the first 5 rows (configurable) and prints them.
    - Spark internally uses a LIMIT pushdown so most partitions are never
      fully scanned; only enough data to satisfy 5 rows is processed.
    - Memory usage on the Driver is negligible (just 5 rows).
    - Safe to call at any stage of development regardless of dataset size.

Rule of thumb:
    Use .show(n) or .take(n) for exploration.
    Use .collect() ONLY after you have verified the result set is small
    (e.g., after groupBy().agg().count() returns a few hundred rows).
"""

# Safe exploration pattern
df.show(5)          # ✅ Safe on any dataset size
# df.collect()      # ❌ DANGEROUS on large datasets – may crash the Driver


# ─────────────────────────────────────────────────────────────────────────────
# Stop the SparkSession
# ─────────────────────────────────────────────────────────────────────────────
spark.stop()
