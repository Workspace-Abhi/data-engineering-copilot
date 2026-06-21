# Data Quality Checkups Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 55: Drift calculation logic in Great Expectations Suite
When implementing `Drift calculation logic` within a `Great Expectations Suite` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Integrate Slack or Teams webhooks to alert teams of critical check failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Metric monitoring in Soda Core Check Engine
When implementing `Metric monitoring` within a `Soda Core Check Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set profile baselines on clean datasets to train quality validation thresholds.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Alerting setups in Pandas Validation Engine
When implementing `Alerting setups` within a `Pandas Validation Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run quality validation checks inside CI/CD pull request tests to avoid staging contamination.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

