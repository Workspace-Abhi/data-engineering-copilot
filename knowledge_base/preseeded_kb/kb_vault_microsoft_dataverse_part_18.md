# Microsoft Dataverse Blueprint Guide - Part 18

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 52: Alternate keys mapping in Alternate Key Mapping
When implementing `Alternate keys mapping` within a `Alternate Key Mapping` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure MSAL authentication using client secrets to retrieve API tokens.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 53: MSAL auth scripts in Dataverse Ingestion SDK
When implementing `MSAL auth scripts` within a `Dataverse Ingestion SDK` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Map source database columns directly to target Dataverse logical names.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 54: OData web queries in OData Query Syntax
When implementing `OData web queries` within a `OData Query Syntax` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure Choice mappings converting string statuses to logical integer codes.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

