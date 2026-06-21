# Data Testing Pipelines Blueprint Guide - Part 10

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 28: Edge validation schemas in CI/CD GitHub Action
When implementing `Edge validation schemas` within a `CI/CD GitHub Action` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure schema drift test checks inside tests to verify column changes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 29: Schema drift testing in Mock Dataset Config
When implementing `Schema drift testing` within a `Mock Dataset Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use pytest-asyncio to mock asynchronous API connection targets.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 30: Parity script tests in SQLite Test Schema
When implementing `Parity script tests` within a `SQLite Test Schema` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build script-based data parity checks validating column ranges and means.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

