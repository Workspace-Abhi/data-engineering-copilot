# Azure Data Factory (ADF) Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 19: Web hook parameters in ADF Pipeline V2
When implementing `Web hook parameters` within a `ADF Pipeline V2` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use dynamic expressions utilizing utcNow() to partition landing directories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Secure input/output in Synapse Pipeline Engine
When implementing `Secure input/output` within a `Synapse Pipeline Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure batch sizes in Copy activity to match source source output limitations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Watermark variables in Azure Data Factory SHIR
When implementing `Watermark variables` within a `Azure Data Factory SHIR` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Lookup activities to retrieve the old watermark value before executing incremental copies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

