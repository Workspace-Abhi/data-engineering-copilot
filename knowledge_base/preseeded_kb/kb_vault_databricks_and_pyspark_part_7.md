# Databricks & PySpark Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 19: SCD Type 2 history in Azure Databricks
When implementing `SCD Type 2 history` within a `Azure Databricks` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure garbage collection parameters using G1GC algorithm for low latency.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Delta Log pruning in AWS EMR Spark
When implementing `Delta Log pruning` within a `AWS EMR Spark` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid PySpark UDFs; rewrite them using SQL native expressions for catalyst compilation.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: AQE tuning in GCP Dataproc
When implementing `AQE tuning` within a `GCP Dataproc` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable adaptive query execution (AQE) to dynamically merge partitions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

