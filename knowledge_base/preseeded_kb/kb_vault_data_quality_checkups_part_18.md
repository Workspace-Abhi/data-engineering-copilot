# Data Quality Checkups Blueprint Guide - Part 18

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 52: Soda core check files in PySpark Check Layer
When implementing `Soda core check files` within a `PySpark Check Layer` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define Soda Core check files containing declarative checks for data profile monitoring.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 53: Schema drift checks in Data Quality Dashboards
When implementing `Schema drift checks` within a `Data Quality Dashboards` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure automated schema drift checks to catch unexpected column addition/deletions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 54: Null validation checks in Slack Alert Webhook
When implementing `Null validation checks` within a `Slack Alert Webhook` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement statistical distribution drift checks (like KS test) to trace numeric drifts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

