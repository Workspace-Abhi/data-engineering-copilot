# Data Quality Checkups Blueprint Guide - Part 13

This documentation blueprint details core rules, best practices, and recipes for `Data Quality Checkups` operations.

### Pattern 37: Alerting setups in Great Expectations Suite
When implementing `Alerting setups` within a `Great Expectations Suite` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run quality validation checks inside CI/CD pull request tests to avoid staging contamination.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 38: Execution profilers in Soda Core Check Engine
When implementing `Execution profilers` within a `Soda Core Check Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Store validation results in a centralized database to plot long-term quality trends.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 39: Baseline validations in Pandas Validation Engine
When implementing `Baseline validations` within a `Pandas Validation Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use custom python assertions to validate complex business logic relationships.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

