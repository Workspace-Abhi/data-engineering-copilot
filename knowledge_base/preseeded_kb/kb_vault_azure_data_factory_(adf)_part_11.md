# Azure Data Factory (ADF) Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 31: Watermark variables in ADF Pipeline V2
When implementing `Watermark variables` within a `ADF Pipeline V2` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Lookup activities to retrieve the old watermark value before executing incremental copies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Pagination rules in Synapse Pipeline Engine
When implementing `Pagination rules` within a `Synapse Pipeline Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement pagination rules on REST API calls utilizing HTTP headers or query parameters.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Activity batching in Azure Data Factory SHIR
When implementing `Activity batching` within a `Azure Data Factory SHIR` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Self-Hosted Integration Runtime (SHIR) auto-scale groups to manage ingestion bandwidth.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

