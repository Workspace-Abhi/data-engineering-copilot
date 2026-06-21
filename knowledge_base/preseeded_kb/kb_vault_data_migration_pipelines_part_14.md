# Data Migration Pipelines Blueprint Guide - Part 14

This documentation blueprint details core rules, best practices, and recipes for `Data Migration Pipelines` operations.

### Pattern 40: Parity checks script in Oracle to Postgres Schema
When implementing `Parity checks script` within a `Oracle to Postgres Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set up dual-run phases to compare production outputs before cutting over.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 41: Cutover planning in ADLS Gen2 Landing
When implementing `Cutover planning` within a `ADLS Gen2 Landing` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Design clear rollback pipelines to reverse replication tasks in case of migration failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 42: Rollback pipelines in Delta Migration Script
When implementing `Rollback pipelines` within a `Delta Migration Script` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize database migration services to sync changes continuously in real-time.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

