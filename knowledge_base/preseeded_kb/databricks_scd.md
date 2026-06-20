# Databricks Delta Lake Slowly Changing Dimensions (SCD) & Performance Optimization

This guide outlines advanced PySpark patterns for Slowly Changing Dimensions (SCD Type 1 & Type 2) and target table optimization rules inside Azure Databricks.

---

## SCD Type 1: Overwrite Matching Rows

SCD Type 1 overwrites existing records directly when changes are detected, keeping only the latest values without historical tracking.

### Implementation Pattern (PySpark Merge)
```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("SCD_Type1").getOrCreate()

def run_scd_type1(source_df, target_path, key_columns, update_columns):
    # Load target delta table
    target_table = DeltaTable.forPath(spark, target_path)
    
    # Build match condition string
    join_condition = " AND ".join([f"target.{col} = source.{col}" for col in key_columns])
    
    # Map update columns
    update_mapping = {col: f"source.{col}" for col in update_columns}
    
    # Execute upsert merge
    target_table.alias("target") \
        .merge(source_df.alias("source"), join_condition) \
        .whenMatchedUpdate(set=update_mapping) \
        .whenNotMatchedInsertAll() \
        .execute()
```

---

## SCD Type 2: History Tracking (Audit Trails)

SCD Type 2 tracks historical changes by maintaining multiple rows for a single natural key. Active records are marked with `is_current = True`, while deactivated old records are marked with `is_current = False` and capped with an `end_date`.

### Implementation Pattern (PySpark Merge)
```python
from delta.tables import DeltaTable
from pyspark.sql.functions import current_date, lit, col

def run_scd_type2(spark, source_df, target_path, key_columns, tracking_columns):
    target_table = DeltaTable.forPath(spark, target_path)
    
    # Step 1: Detect updates to existing current rows and expire them
    expire_condition = " AND ".join([f"target.{col} = source.{col}" for col in key_columns])
    expire_condition += " AND target.is_current = true"
    
    target_table.alias("target").merge(
        source_df.alias("source"),
        expire_condition
    ).whenMatchedUpdate(set={
        "end_date": "current_date() - 1",
        "is_current": "lit(false)"
    }).execute()
    
    # Step 2: Append all incoming rows as new current active entries
    new_records = source_df \
        .withColumn("start_date", current_date()) \
        .withColumn("end_date", lit(None).cast("date")) \
        .withColumn("is_current", lit(True))
        
    new_records.write.format("delta").mode("append").save(target_path)
```

---

## Delta Table Performance Optimization

To maintain sub-second queries on multi-million row Delta tables, developers must apply compaction and data-skipping rules:

### Z-Order Compaction
Z-Ordering dynamically clusters related information in the same physical files, maximizing the efficiency of file-skipping under WHERE clauses.
```sql
OPTIMIZE delta_db.dim_customers
ZORDER BY (customer_id, country_code);
```

### Auto-Optimize Settings
Enable automated background optimization to prevent the "small file problem" during micro-batch operations:
```sql
ALTER TABLE delta_db.dim_customers SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);
```

### Clean Up Stale Files (Vacuuming)
Periodically delete files that are no longer in the active transaction log to save storage:
```sql
VACUUM delta_db.dim_customers RETAIN 168 HOURS; -- Retains 7 days of historical logs
```
