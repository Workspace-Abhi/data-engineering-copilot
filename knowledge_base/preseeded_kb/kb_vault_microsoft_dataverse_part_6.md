# Microsoft Dataverse Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 16: Ingestion scripts python in Alternate Key Mapping
When implementing `Ingestion scripts python` within a `Alternate Key Mapping` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Verify entity relationships schema before designing batch load payloads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: API link parameters in Dataverse Ingestion SDK
When implementing `API link parameters` within a `Dataverse Ingestion SDK` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure service principal properties on Dataverse before initiating connections.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: SDK patch payload in OData Query Syntax
When implementing `SDK patch payload` within a `OData Query Syntax` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write python SDK scripts utilizing PATCH requests to upsert records.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

