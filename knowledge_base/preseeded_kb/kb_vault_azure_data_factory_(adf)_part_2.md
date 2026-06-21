# Azure Data Factory (ADF) Blueprint Guide - Part 2

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 4: SHIR scalability in Mapping Data Flow Engine
When implementing `SHIR scalability` within a `Mapping Data Flow Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Parameterize linked services connection string to point dynamically to database environments.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 5: Retry triggers in ADF Copy Activity
When implementing `Retry triggers` within a `ADF Copy Activity` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set secure input/output check flags to conceal API keys or secrets in logs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 6: Mapping Data Flows in Linked Service Core
When implementing `Mapping Data Flows` within a `Linked Service Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure execution retry counts and intervals to recover from transient failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

