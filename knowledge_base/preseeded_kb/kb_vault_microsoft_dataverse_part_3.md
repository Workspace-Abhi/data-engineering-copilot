# Microsoft Dataverse Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 7: API link parameters in Dataverse Web API
When implementing `API link parameters` within a `Dataverse Web API` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure service principal properties on Dataverse before initiating connections.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: SDK patch payload in MSAL Authentication Python
When implementing `SDK patch payload` within a `MSAL Authentication Python` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write python SDK scripts utilizing PATCH requests to upsert records.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: Entity relations schema in Choice Configuration Sheet
When implementing `Entity relations schema` within a `Choice Configuration Sheet` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use $filter queries to retrieve specific entities from OData endpoints.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

