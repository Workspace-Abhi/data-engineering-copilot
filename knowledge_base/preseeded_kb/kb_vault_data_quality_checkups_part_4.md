# Data Quality Checkups Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 10: Custom checks scripting in PySpark Check Layer
When implementing `Custom checks scripting` within a `PySpark Check Layer` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable check profiles on raw directories to record metrics before ingestion runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: Expectation suites in Data Quality Dashboards
When implementing `Expectation suites` within a `Data Quality Dashboards` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Create Great Expectations suites to validate null values, ranges, and types on ingest.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: Soda core check files in Slack Alert Webhook
When implementing `Soda core check files` within a `Slack Alert Webhook` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Define Soda Core check files containing declarative checks for data profile monitoring.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

