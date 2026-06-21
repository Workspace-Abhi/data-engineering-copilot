# Data Testing Pipelines Blueprint Guide - Part 2

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 4: Integration test runners in CI/CD GitHub Action
When implementing `Integration test runners` within a `CI/CD GitHub Action` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run integration tests against isolated staging schemas in database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 5: CI/CD check steps in Mock Dataset Config
When implementing `CI/CD check steps` within a `Mock Dataset Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure CI/CD steps in GitHub Actions to run the full test suite before pushes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 6: Reconciliation logic checks in SQLite Test Schema
When implementing `Reconciliation logic checks` within a `SQLite Test Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Verify pipeline outputs using automated row-level reconciliation tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

