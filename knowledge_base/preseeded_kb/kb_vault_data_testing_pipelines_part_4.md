# Data Testing Pipelines Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 10: Parity script tests in CI/CD GitHub Action
When implementing `Parity script tests` within a `CI/CD GitHub Action` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build script-based data parity checks validating column ranges and means.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: Unit testing setups in Mock Dataset Config
When implementing `Unit testing setups` within a `Mock Dataset Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write pytest unit tests to validate custom pandas transformations and edge case inputs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: Mock datasets CSV in SQLite Test Schema
When implementing `Mock datasets CSV` within a `SQLite Test Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Generate mock datasets in CSV or JSON format to test pipeline logic locally.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

