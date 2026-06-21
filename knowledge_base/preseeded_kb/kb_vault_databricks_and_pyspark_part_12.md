# Databricks & PySpark Blueprint Guide - Part 12

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 34: Delta vacuum policy in Local PySpark Engine
When implementing `Delta vacuum policy` within a `Local PySpark Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run OPTIMIZE with ZORDER BY on query lookup keys to speed up folder pruning.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 35: Broadcast joins in Delta Lake 3.0
When implementing `Broadcast joins` within a `Delta Lake 3.0` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Apply delta table VACUUM retaining 168 hours to clean orphaned parquet files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 36: Memory tuning in Unity Catalog Hub
When implementing `Memory tuning` within a `Unity Catalog Hub` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Spark Structured Streaming checkpointing to guarantee once-only delivery.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

