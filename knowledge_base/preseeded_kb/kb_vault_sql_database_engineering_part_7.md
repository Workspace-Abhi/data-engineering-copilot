# SQL Database Engineering Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 19: Index Coverage in SQL Server / Synapse
When implementing `Index Coverage` within a `SQL Server / Synapse` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid nested subqueries; convert them to CTEs or Joins for cost optimization.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Covering Indexes in PostgreSQL
When implementing `Covering Indexes` within a `PostgreSQL` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set fill factor to 80% on high-write primary keys to reduce page splits.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Index Tuning in Snowflake
When implementing `Index Tuning` within a `Snowflake` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use non-clustered index on filter columns to eliminate table scans.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

