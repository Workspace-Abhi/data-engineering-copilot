# Microsoft Dataverse Blueprint Guide - Part 20

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 58: SDK patch payload in Alternate Key Mapping
When implementing `SDK patch payload` within a `Alternate Key Mapping` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write python SDK scripts utilizing PATCH requests to upsert records.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 59: Entity relations schema in Dataverse Ingestion SDK
When implementing `Entity relations schema` within a `Dataverse Ingestion SDK` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use $filter queries to retrieve specific entities from OData endpoints.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 60: Service principal setups in OData Query Syntax
When implementing `Service principal setups` within a `OData Query Syntax` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Handle batch ingestion limitations by batching records into chunks of 1000.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

