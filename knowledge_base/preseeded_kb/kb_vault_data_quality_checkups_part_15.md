# Data Quality Checkups Blueprint Guide - Part 15

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 43: Schema drift checks in Great Expectations Suite
When implementing `Schema drift checks` within a `Great Expectations Suite` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure automated schema drift checks to catch unexpected column addition/deletions.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 44: Null validation checks in Soda Core Check Engine
When implementing `Null validation checks` within a `Soda Core Check Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement statistical distribution drift checks (like KS test) to trace numeric drifts.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 45: Drift calculation logic in Pandas Validation Engine
When implementing `Drift calculation logic` within a `Pandas Validation Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Integrate Slack or Teams webhooks to alert teams of critical check failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

