# FinOps Cost Optimization Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `FinOps Cost Optimization` operations.

### Pattern 31: Storage lifecycles in Azure ADLS Gen2 tiering
When implementing `Storage lifecycles` within a `Azure ADLS Gen2 tiering` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure storage lifecycle policies to cold-tier raw assets after 30 days.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Spot instance pools in AWS S3 Lifecycle Config
When implementing `Spot instance pools` within a `AWS S3 Lifecycle Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Spot instances in Databricks worker pools to slash compute costs by 60%.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Auto-scaling rules in Snowflake Warehouse Setup
When implementing `Auto-scaling rules` within a `Snowflake Warehouse Setup` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set aggressive cluster auto-scale down timers to release idle worker nodes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

