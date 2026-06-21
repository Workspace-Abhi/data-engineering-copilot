# Databricks & PySpark Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 22: Skew Join Mitigation in Local PySpark Engine
When implementing `Skew Join Mitigation` within a `Local PySpark Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use broadcast hints on small tables to eliminate shuffle bottlenecks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: Z-Ordering compaction in Delta Lake 3.0
When implementing `Z-Ordering compaction` within a `Delta Lake 3.0` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement skew join hints detailing the specific skewed column to balance partition distribution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: Delta vacuum policy in Unity Catalog Hub
When implementing `Delta vacuum policy` within a `Unity Catalog Hub` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run OPTIMIZE with ZORDER BY on query lookup keys to speed up folder pruning.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

