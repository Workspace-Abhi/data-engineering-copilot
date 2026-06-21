# Databricks & PySpark Blueprint Guide - Part 16

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 46: Memory tuning in Local PySpark Engine
When implementing `Memory tuning` within a `Local PySpark Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Spark Structured Streaming checkpointing to guarantee once-only delivery.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 47: GC overhead in Delta Lake 3.0
When implementing `GC overhead` within a `Delta Lake 3.0` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Tweak spark.sql.shuffle.partitions dynamically to match executor cores count.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 48: Checkpoint stores in Unity Catalog Hub
When implementing `Checkpoint stores` within a `Unity Catalog Hub` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Delta Lake merge schemas to allow schema drift safely.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

