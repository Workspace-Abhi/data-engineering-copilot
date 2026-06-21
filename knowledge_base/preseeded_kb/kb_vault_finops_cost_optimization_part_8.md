# FinOps Cost Optimization Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 22: Spot instance pools in Databricks Cluster Manager
When implementing `Spot instance pools` within a `Databricks Cluster Manager` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Spot instances in Databricks worker pools to slash compute costs by 60%.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: Auto-scaling rules in BigQuery Storage Saver
When implementing `Auto-scaling rules` within a `BigQuery Storage Saver` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set aggressive cluster auto-scale down timers to release idle worker nodes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: Warehouse sizing in FinOps Billing Portal
When implementing `Warehouse sizing` within a `FinOps Billing Portal` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Optimize partition pruning index structures to avoid costly scanning overheads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

