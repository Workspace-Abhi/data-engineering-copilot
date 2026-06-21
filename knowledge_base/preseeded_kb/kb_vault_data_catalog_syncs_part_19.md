# Data Catalog Syncs Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 55: OpenLineage integrations in Collibra API Catalog
When implementing `OpenLineage integrations` within a `Collibra API Catalog` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Synchronize data models to Collibra using custom REST API connector configs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Table descriptions tags in Apache Atlas Metadata
When implementing `Table descriptions tags` within a `Apache Atlas Metadata` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Update table description tags programmatically within databases during dbt runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Asset categorizations in Azure Purview API
When implementing `Asset categorizations` within a `Azure Purview API` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure asset search tags to locate data assets based on categories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

