# FinOps Cost Optimization Blueprint Guide - Part 2

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 4: Warehouse sizing in Databricks Cluster Manager
When implementing `Warehouse sizing` within a `Databricks Cluster Manager` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Optimize partition pruning index structures to avoid costly scanning overheads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 5: Partition pruning index in BigQuery Storage Saver
When implementing `Partition pruning index` within a `BigQuery Storage Saver` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable auto-suspend timers (e.g. 60 seconds) on Snowflake compute warehouses.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 6: Compression format in FinOps Billing Portal
When implementing `Compression format` within a `FinOps Billing Portal` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use ZSTD or Snappy compression formats to save storage space and I/O costs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

