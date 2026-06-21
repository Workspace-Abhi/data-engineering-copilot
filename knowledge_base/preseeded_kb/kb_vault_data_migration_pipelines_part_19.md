# Data Migration Pipelines Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Data Migration Pipelines` operations.

### Pattern 55: Landing zone configs in AWS DMS Sync
When implementing `Landing zone configs` within a `AWS DMS Sync` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Partition historical load pipelines into chunks to avoid database timeouts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Historical load pipelines in Azure Data Box Ingestion
When implementing `Historical load pipelines` within a `Azure Data Box Ingestion` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement delta sync logic utilizing modified dates to sync changes post-initial load.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Delta sync logic in Snowflake Snowpipe Engine
When implementing `Delta sync logic` within a `Snowflake Snowpipe Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable parallel ingestion runs to accelerate data replication over large tables.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

