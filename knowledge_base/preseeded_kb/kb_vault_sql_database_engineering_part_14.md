# SQL Database Engineering Blueprint Guide - Part 14

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 40: Covering Indexes in Google BigQuery
When implementing `Covering Indexes` within a `Google BigQuery` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set fill factor to 80% on high-write primary keys to reduce page splits.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 41: Index Tuning in Oracle DB
When implementing `Index Tuning` within a `Oracle DB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use non-clustered index on filter columns to eliminate table scans.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 42: Recursive CTEs in MySQL InnoDB
When implementing `Recursive CTEs` within a `MySQL InnoDB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize recursive CTEs with MAXRECURSION limit to prevent infinite loops.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

