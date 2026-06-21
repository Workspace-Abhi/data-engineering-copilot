# Databricks & PySpark Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 7: GC overhead in Azure Databricks
When implementing `GC overhead` within a `Azure Databricks` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Tweak spark.sql.shuffle.partitions dynamically to match executor cores count.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: Checkpoint stores in AWS EMR Spark
When implementing `Checkpoint stores` within a `AWS EMR Spark` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Delta Lake merge schemas to allow schema drift safely.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: SCD Type 2 history in GCP Dataproc
When implementing `SCD Type 2 history` within a `GCP Dataproc` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure garbage collection parameters using G1GC algorithm for low latency.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

