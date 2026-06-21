# SQL Database Engineering Blueprint Guide - Part 12

This documentation blueprint details core rules, best practices, and recipes for `SQL Database Engineering` operations.

### Pattern 34: CDC Triggers in Google BigQuery
When implementing `CDC Triggers` within a `Google BigQuery` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement CDC query filters targeting modified LSN boundaries.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 35: Lock Escalations in Oracle DB
When implementing `Lock Escalations` within a `Oracle DB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure snapshot isolation levels to eliminate reader-writer blockages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 36: Execution Plans in MySQL InnoDB
When implementing `Execution Plans` within a `MySQL InnoDB` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Validate execution plan cost metrics to locate Cartesian join operations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

