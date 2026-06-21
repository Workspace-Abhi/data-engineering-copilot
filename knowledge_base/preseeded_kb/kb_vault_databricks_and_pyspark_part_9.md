# Databricks & PySpark Blueprint Guide - Part 9

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 25: Broadcast joins in Azure Databricks
When implementing `Broadcast joins` within a `Azure Databricks` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Apply delta table VACUUM retaining 168 hours to clean orphaned parquet files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 26: Memory tuning in AWS EMR Spark
When implementing `Memory tuning` within a `AWS EMR Spark` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Spark Structured Streaming checkpointing to guarantee once-only delivery.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 27: GC overhead in GCP Dataproc
When implementing `GC overhead` within a `GCP Dataproc` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Tweak spark.sql.shuffle.partitions dynamically to match executor cores count.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

