# Azure Data Factory (ADF) Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `Azure Data Factory (ADF)` operations.

### Pattern 10: Secure input/output in Mapping Data Flow Engine
When implementing `Secure input/output` within a `Mapping Data Flow Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure batch sizes in Copy activity to match source source output limitations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: Watermark variables in ADF Copy Activity
When implementing `Watermark variables` within a `ADF Copy Activity` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use Lookup activities to retrieve the old watermark value before executing incremental copies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: Pagination rules in Linked Service Core
When implementing `Pagination rules` within a `Linked Service Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement pagination rules on REST API calls utilizing HTTP headers or query parameters.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

