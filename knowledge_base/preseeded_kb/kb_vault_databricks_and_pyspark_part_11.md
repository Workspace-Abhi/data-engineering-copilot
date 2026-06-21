# Databricks & PySpark Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Databricks & PySpark` operations.

### Pattern 31: AQE tuning in Azure Databricks
When implementing `AQE tuning` within a `Azure Databricks` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable adaptive query execution (AQE) to dynamically merge partitions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Skew Join Mitigation in AWS EMR Spark
When implementing `Skew Join Mitigation` within a `AWS EMR Spark` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use broadcast hints on small tables to eliminate shuffle bottlenecks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Z-Ordering compaction in GCP Dataproc
When implementing `Z-Ordering compaction` within a `GCP Dataproc` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement skew join hints detailing the specific skewed column to balance partition distribution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

