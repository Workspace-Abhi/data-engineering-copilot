# Data Catalog Syncs Blueprint Guide - Part 6

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 16: Table descriptions tags in Amundsen Metadata Config
When implementing `Table descriptions tags` within a `Amundsen Metadata Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Update table description tags programmatically within databases during dbt runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 17: Asset categorizations in Alation Catalog Connector
When implementing `Asset categorizations` within a `Alation Catalog Connector` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure asset search tags to locate data assets based on categories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 18: Owner tag configs in OpenLineage Standard Docs
When implementing `Owner tag configs` within a `OpenLineage Standard Docs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Establish owner tag configurations to assign data assets to specific teams.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

