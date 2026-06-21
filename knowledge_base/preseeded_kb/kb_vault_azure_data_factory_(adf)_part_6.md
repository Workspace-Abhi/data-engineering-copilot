# Azure Data Factory (ADF) Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 16: Mapping Data Flows in Mapping Data Flow Engine
When implementing `Mapping Data Flows` within a `Mapping Data Flow Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure execution retry counts and intervals to recover from transient failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: Event triggers in ADF Copy Activity
When implementing `Event triggers` within a `ADF Copy Activity` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize Mapping Data Flows for non-code visual conversions at scale.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: Linked services parameters in Linked Service Core
When implementing `Linked services parameters` within a `Linked Service Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement validation activities to check file presence before execution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

