# Databricks & PySpark Blueprint Guide - Part 14

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 40: Delta Log pruning in Local PySpark Engine
When implementing `Delta Log pruning` within a `Local PySpark Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid PySpark UDFs; rewrite them using SQL native expressions for catalyst compilation.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 41: AQE tuning in Delta Lake 3.0
When implementing `AQE tuning` within a `Delta Lake 3.0` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable adaptive query execution (AQE) to dynamically merge partitions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 42: Skew Join Mitigation in Unity Catalog Hub
When implementing `Skew Join Mitigation` within a `Unity Catalog Hub` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use broadcast hints on small tables to eliminate shuffle bottlenecks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

