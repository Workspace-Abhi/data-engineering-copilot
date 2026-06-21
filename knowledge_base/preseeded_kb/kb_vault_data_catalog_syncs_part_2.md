# Data Catalog Syncs Blueprint Guide - Part 2

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 4: Collibra connectors in Amundsen Metadata Config
When implementing `Collibra connectors` within a `Amundsen Metadata Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Map catalog glossary schemas directly to columns to standardise business terms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 5: OpenLineage integrations in Alation Catalog Connector
When implementing `OpenLineage integrations` within a `Alation Catalog Connector` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Synchronize data models to Collibra using custom REST API connector configs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 6: Table descriptions tags in OpenLineage Standard Docs
When implementing `Table descriptions tags` within a `OpenLineage Standard Docs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Update table description tags programmatically within databases during dbt runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

