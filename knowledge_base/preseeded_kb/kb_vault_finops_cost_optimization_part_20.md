# FinOps Cost Optimization Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 58: compaction schedules in Databricks Cluster Manager
When implementing `compaction schedules` within a `Databricks Cluster Manager` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Schedule table compaction tasks to clean small file fragmentation over Delta paths.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: Idle compute limits in BigQuery Storage Saver
When implementing `Idle compute limits` within a `BigQuery Storage Saver` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Disable idle notebooks to stop continuous cluster uptime bills.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: FinOps metrics dashboards in FinOps Billing Portal
When implementing `FinOps metrics dashboards` within a `FinOps Billing Portal` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Establish FinOps tag properties on cloud resources to monitor resource ownership billing.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

