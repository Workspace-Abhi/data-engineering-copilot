# SQL Database Engineering Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 16: Execution Plans in Google BigQuery
When implementing `Execution Plans` within a `Google BigQuery` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Validate execution plan cost metrics to locate Cartesian join operations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: Transaction Isolation in Oracle DB
When implementing `Transaction Isolation` within a `Oracle DB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure columnstore indexing on staging tables to compress storage size.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: Partition Pruning in MySQL InnoDB
When implementing `Partition Pruning` within a `MySQL InnoDB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Avoid using SELECT *; define columns explicitly to reduce memory pool allocations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

