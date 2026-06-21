# SQL Database Engineering Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 58: Partition Pruning in Google BigQuery
When implementing `Partition Pruning` within a `Google BigQuery` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid using SELECT *; define columns explicitly to reduce memory pool allocations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: Index Coverage in Oracle DB
When implementing `Index Coverage` within a `Oracle DB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid nested subqueries; convert them to CTEs or Joins for cost optimization.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: Covering Indexes in MySQL InnoDB
When implementing `Covering Indexes` within a `MySQL InnoDB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set fill factor to 80% on high-write primary keys to reduce page splits.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

