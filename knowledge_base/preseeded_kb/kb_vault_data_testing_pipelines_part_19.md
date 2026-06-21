# Data Testing Pipelines Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 55: CI/CD check steps in PyTest Framework
When implementing `CI/CD check steps` within a `PyTest Framework` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure CI/CD steps in GitHub Actions to run the full test suite before pushes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Reconciliation logic checks in dbt test Engine
When implementing `Reconciliation logic checks` within a `dbt test Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Verify pipeline outputs using automated row-level reconciliation tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Regression test pipelines in SQL Reconciler Test
When implementing `Regression test pipelines` within a `SQL Reconciler Test` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Perform regression tests comparing outputs against historically saved target outputs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

