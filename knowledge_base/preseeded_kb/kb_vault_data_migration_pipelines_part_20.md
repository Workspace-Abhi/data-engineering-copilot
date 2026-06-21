# Data Migration Pipelines Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `Data Migration Pipelines` operations.

### Pattern 58: Parallel ingestion pipelines in Oracle to Postgres Schema
When implementing `Parallel ingestion pipelines` within a `Oracle to Postgres Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Validate parity check metrics (row counts, checksums) to confirm migration fidelity.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: Validation checks DDL in ADLS Gen2 Landing
When implementing `Validation checks DDL` within a `ADLS Gen2 Landing` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Snowpipe or direct triggers to auto-ingest incoming cutover delta files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: Parity checks script in Delta Migration Script
When implementing `Parity checks script` within a `Delta Migration Script` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set up dual-run phases to compare production outputs before cutting over.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

