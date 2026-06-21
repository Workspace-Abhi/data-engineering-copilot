# Data Testing Pipelines Blueprint Guide - Part 16

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 46: Reconciliation logic checks in CI/CD GitHub Action
When implementing `Reconciliation logic checks` within a `CI/CD GitHub Action` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Verify pipeline outputs using automated row-level reconciliation tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 47: Regression test pipelines in Mock Dataset Config
When implementing `Regression test pipelines` within a `Mock Dataset Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Perform regression tests comparing outputs against historically saved target outputs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 48: Edge validation schemas in SQLite Test Schema
When implementing `Edge validation schemas` within a `SQLite Test Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure schema drift test checks inside tests to verify column changes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

