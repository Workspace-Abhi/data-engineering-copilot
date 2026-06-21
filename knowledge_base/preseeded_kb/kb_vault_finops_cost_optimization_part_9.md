# FinOps Cost Optimization Blueprint Guide - Part 9

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 25: Partition pruning index in Azure ADLS Gen2 tiering
When implementing `Partition pruning index` within a `Azure ADLS Gen2 tiering` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable auto-suspend timers (e.g. 60 seconds) on Snowflake compute warehouses.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 26: Compression format in AWS S3 Lifecycle Config
When implementing `Compression format` within a `AWS S3 Lifecycle Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use ZSTD or Snappy compression formats to save storage space and I/O costs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 27: Billing alerts in Snowflake Warehouse Setup
When implementing `Billing alerts` within a `Snowflake Warehouse Setup` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set up alerts for daily billing deviations to catch runaway recursion runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

