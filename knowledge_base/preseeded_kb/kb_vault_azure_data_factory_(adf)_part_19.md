# Azure Data Factory (ADF) Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 55: Retry triggers in ADF Pipeline V2
When implementing `Retry triggers` within a `ADF Pipeline V2` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set secure input/output check flags to conceal API keys or secrets in logs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Mapping Data Flows in Synapse Pipeline Engine
When implementing `Mapping Data Flows` within a `Synapse Pipeline Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure execution retry counts and intervals to recover from transient failures.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Event triggers in Azure Data Factory SHIR
When implementing `Event triggers` within a `Azure Data Factory SHIR` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize Mapping Data Flows for non-code visual conversions at scale.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

