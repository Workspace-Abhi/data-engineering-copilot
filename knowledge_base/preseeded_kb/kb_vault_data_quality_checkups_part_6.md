# Data Quality Checkups Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 16: Metric monitoring in PySpark Check Layer
When implementing `Metric monitoring` within a `PySpark Check Layer` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set profile baselines on clean datasets to train quality validation thresholds.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: Alerting setups in Data Quality Dashboards
When implementing `Alerting setups` within a `Data Quality Dashboards` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run quality validation checks inside CI/CD pull request tests to avoid staging contamination.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: Execution profilers in Slack Alert Webhook
When implementing `Execution profilers` within a `Slack Alert Webhook` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Store validation results in a centralized database to plot long-term quality trends.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

