# FinOps Cost Optimization Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 16: Compression format in Databricks Cluster Manager
When implementing `Compression format` within a `Databricks Cluster Manager` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use ZSTD or Snappy compression formats to save storage space and I/O costs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: Billing alerts in BigQuery Storage Saver
When implementing `Billing alerts` within a `BigQuery Storage Saver` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set up alerts for daily billing deviations to catch runaway recursion runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: compaction schedules in FinOps Billing Portal
When implementing `compaction schedules` within a `FinOps Billing Portal` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Schedule table compaction tasks to clean small file fragmentation over Delta paths.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

