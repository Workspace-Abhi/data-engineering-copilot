# Data Testing Pipelines Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 22: Mock datasets CSV in CI/CD GitHub Action
When implementing `Mock datasets CSV` within a `CI/CD GitHub Action` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Generate mock datasets in CSV or JSON format to test pipeline logic locally.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: SQL assertion schemas in Mock Dataset Config
When implementing `SQL assertion schemas` within a `Mock Dataset Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement SQL assertion schemas to check for duplicate keys in target tables.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: Integration test runners in SQLite Test Schema
When implementing `Integration test runners` within a `SQLite Test Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Run integration tests against isolated staging schemas in database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

