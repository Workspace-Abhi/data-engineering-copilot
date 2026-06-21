# SQL Database Engineering Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 22: Recursive CTEs in Google BigQuery
When implementing `Recursive CTEs` within a `Google BigQuery` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize recursive CTEs with MAXRECURSION limit to prevent infinite loops.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: Window Grouping in Oracle DB
When implementing `Window Grouping` within a `Oracle DB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Apply DENSE_RANK() over partition key to resolve deduplication criteria.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: CDC Triggers in MySQL InnoDB
When implementing `CDC Triggers` within a `MySQL InnoDB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement CDC query filters targeting modified LSN boundaries.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

