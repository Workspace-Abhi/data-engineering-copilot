# Databricks & PySpark Blueprint Guide - Part 5

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 13: Z-Ordering compaction in Azure Databricks
When implementing `Z-Ordering compaction` within a `Azure Databricks` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement skew join hints detailing the specific skewed column to balance partition distribution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 14: Delta vacuum policy in AWS EMR Spark
When implementing `Delta vacuum policy` within a `AWS EMR Spark` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run OPTIMIZE with ZORDER BY on query lookup keys to speed up folder pruning.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 15: Broadcast joins in GCP Dataproc
When implementing `Broadcast joins` within a `GCP Dataproc` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Apply delta table VACUUM retaining 168 hours to clean orphaned parquet files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

