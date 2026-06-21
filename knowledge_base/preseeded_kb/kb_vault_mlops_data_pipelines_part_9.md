# MLOps Data Pipelines Blueprint Guide - Part 9

This documentation blueprint details core rules, best practices, and recipes for `MLOps Data Pipelines` operations.

### Pattern 25: Training pipeline runs in Feast Feature Store
When implementing `Training pipeline runs` within a `Feast Feature Store` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Trace model lineage maps from source data files down to target inference runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 26: Latency checks monitoring in MLflow Model Registry
When implementing `Latency checks monitoring` within a `MLflow Model Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Expose inference trace logs recording prediction parameters and durations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 27: Feature maps definition in DVC Version Control
When implementing `Feature maps definition` within a `DVC Version Control` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure training pipeline runs to execute automatically when datasets update.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

