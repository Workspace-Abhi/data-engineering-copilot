# Data Catalog Syncs Blueprint Guide - Part 5

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 13: Lineage traversers in Collibra API Catalog
When implementing `Lineage traversers` within a `Collibra API Catalog` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable OpenLineage integrations in Spark to trace parent-child table linkages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 14: Collibra connectors in Apache Atlas Metadata
When implementing `Collibra connectors` within a `Apache Atlas Metadata` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Map catalog glossary schemas directly to columns to standardise business terms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 15: OpenLineage integrations in Azure Purview API
When implementing `OpenLineage integrations` within a `Azure Purview API` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Synchronize data models to Collibra using custom REST API connector configs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

