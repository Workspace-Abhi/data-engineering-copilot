# Data Testing Pipelines Blueprint Guide - Part 13

This documentation blueprint details core rules, best practices, and recipes for `Data Testing Pipelines` operations.

### Pattern 37: Regression test pipelines in PyTest Framework
When implementing `Regression test pipelines` within a `PyTest Framework` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Perform regression tests comparing outputs against historically saved target outputs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 38: Edge validation schemas in dbt test Engine
When implementing `Edge validation schemas` within a `dbt test Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure schema drift test checks inside tests to verify column changes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 39: Schema drift testing in SQL Reconciler Test
When implementing `Schema drift testing` within a `SQL Reconciler Test` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use pytest-asyncio to mock asynchronous API connection targets.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

