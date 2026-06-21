# Databricks & PySpark Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 58: Checkpoint stores in Local PySpark Engine
When implementing `Checkpoint stores` within a `Local PySpark Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Delta Lake merge schemas to allow schema drift safely.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: SCD Type 2 history in Delta Lake 3.0
When implementing `SCD Type 2 history` within a `Delta Lake 3.0` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure garbage collection parameters using G1GC algorithm for low latency.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: Delta Log pruning in Unity Catalog Hub
When implementing `Delta Log pruning` within a `Unity Catalog Hub` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid PySpark UDFs; rewrite them using SQL native expressions for catalyst compilation.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

