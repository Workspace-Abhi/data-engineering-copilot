# Microsoft Dataverse Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `Microsoft Dataverse` operations.

### Pattern 10: Service principal setups in Alternate Key Mapping
When implementing `Service principal setups` within a `Alternate Key Mapping` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Handle batch ingestion limitations by batching records into chunks of 1000.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: Entity mappings DDL in Dataverse Ingestion SDK
When implementing `Entity mappings DDL` within a `Dataverse Ingestion SDK` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement OData alternate keys to patch Dataverse entities without checking IDs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: Alternate keys mapping in OData Query Syntax
When implementing `Alternate keys mapping` within a `OData Query Syntax` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure MSAL authentication using client secrets to retrieve API tokens.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

