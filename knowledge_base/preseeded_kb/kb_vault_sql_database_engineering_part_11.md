# SQL Database Engineering Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 31: Index Tuning in SQL Server / Synapse
When implementing `Index Tuning` within a `SQL Server / Synapse` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use non-clustered index on filter columns to eliminate table scans.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Recursive CTEs in PostgreSQL
When implementing `Recursive CTEs` within a `PostgreSQL` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize recursive CTEs with MAXRECURSION limit to prevent infinite loops.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Window Grouping in Snowflake
When implementing `Window Grouping` within a `Snowflake` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Apply DENSE_RANK() over partition key to resolve deduplication criteria.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

