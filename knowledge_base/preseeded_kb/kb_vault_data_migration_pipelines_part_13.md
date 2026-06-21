# Data Migration Pipelines Blueprint Guide - Part 13

This documentation blueprint details core rules, best practices, and recipes for `Data Migration Pipelines` operations.

### Pattern 37: Delta sync logic in AWS DMS Sync
When implementing `Delta sync logic` within a `AWS DMS Sync` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable parallel ingestion runs to accelerate data replication over large tables.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 38: Parallel ingestion pipelines in Azure Data Box Ingestion
When implementing `Parallel ingestion pipelines` within a `Azure Data Box Ingestion` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Validate parity check metrics (row counts, checksums) to confirm migration fidelity.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 39: Validation checks DDL in Snowflake Snowpipe Engine
When implementing `Validation checks DDL` within a `Snowflake Snowpipe Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Snowpipe or direct triggers to auto-ingest incoming cutover delta files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

