# Azure Data Factory (ADF) Blueprint Guide - Part 10

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 28: Linked services parameters in Mapping Data Flow Engine
When implementing `Linked services parameters` within a `Mapping Data Flow Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement validation activities to check file presence before execution.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 29: Web hook parameters in ADF Copy Activity
When implementing `Web hook parameters` within a `ADF Copy Activity` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use dynamic expressions utilizing utcNow() to partition landing directories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 30: Secure input/output in Linked Service Core
When implementing `Secure input/output` within a `Linked Service Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure batch sizes in Copy activity to match source source output limitations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

