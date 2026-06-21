# Microsoft Dataverse Blueprint Guide - Part 12

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 34: OData web queries in Alternate Key Mapping
When implementing `OData web queries` within a `Alternate Key Mapping` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Choice mappings converting string statuses to logical integer codes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 35: Choice mappings config in Dataverse Ingestion SDK
When implementing `Choice mappings config` within a `Dataverse Ingestion SDK` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Create alternate keys on target entity fields to resolve relationship mappings.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 36: Ingestion scripts python in OData Query Syntax
When implementing `Ingestion scripts python` within a `OData Query Syntax` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Verify entity relationships schema before designing batch load payloads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

