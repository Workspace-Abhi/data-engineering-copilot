# Data Migration Pipelines Blueprint Guide - Part 17

This documentation blueprint details core rules, best practices, and recipes for `Data Migration Pipelines` operations.

### Pattern 49: Validation checks DDL in AWS DMS Sync
When implementing `Validation checks DDL` within a `AWS DMS Sync` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Snowpipe or direct triggers to auto-ingest incoming cutover delta files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 50: Parity checks script in Azure Data Box Ingestion
When implementing `Parity checks script` within a `Azure Data Box Ingestion` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set up dual-run phases to compare production outputs before cutting over.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 51: Cutover planning in Snowflake Snowpipe Engine
When implementing `Cutover planning` within a `Snowflake Snowpipe Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Design clear rollback pipelines to reverse replication tasks in case of migration failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

