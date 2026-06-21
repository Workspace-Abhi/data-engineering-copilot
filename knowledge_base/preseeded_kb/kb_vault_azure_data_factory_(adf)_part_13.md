# Azure Data Factory (ADF) Blueprint Guide - Part 13

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 37: Event triggers in ADF Pipeline V2
When implementing `Event triggers` within a `ADF Pipeline V2` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize Mapping Data Flows for non-code visual conversions at scale.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 38: Linked services parameters in Synapse Pipeline Engine
When implementing `Linked services parameters` within a `Synapse Pipeline Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement validation activities to check file presence before execution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 39: Web hook parameters in Azure Data Factory SHIR
When implementing `Web hook parameters` within a `Azure Data Factory SHIR` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use dynamic expressions utilizing utcNow() to partition landing directories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

