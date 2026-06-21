# Data Testing Pipelines Blueprint Guide - Part 5

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 13: SQL assertion schemas in PyTest Framework
When implementing `SQL assertion schemas` within a `PyTest Framework` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement SQL assertion schemas to check for duplicate keys in target tables.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 14: Integration test runners in dbt test Engine
When implementing `Integration test runners` within a `dbt test Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run integration tests against isolated staging schemas in database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 15: CI/CD check steps in SQL Reconciler Test
When implementing `CI/CD check steps` within a `SQL Reconciler Test` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure CI/CD steps in GitHub Actions to run the full test suite before pushes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

