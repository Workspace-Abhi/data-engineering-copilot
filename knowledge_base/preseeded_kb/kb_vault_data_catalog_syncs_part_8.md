# Data Catalog Syncs Blueprint Guide - Part 8

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 22: Data dictionaries MD in Amundsen Metadata Config
When implementing `Data dictionaries MD` within a `Amundsen Metadata Config` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Publish data dictionaries in markdown format to build repository search directories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 23: Lineage traversers in Alation Catalog Connector
When implementing `Lineage traversers` within a `Alation Catalog Connector` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable OpenLineage integrations in Spark to trace parent-child table linkages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 24: Collibra connectors in OpenLineage Standard Docs
When implementing `Collibra connectors` within a `OpenLineage Standard Docs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Map catalog glossary schemas directly to columns to standardise business terms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

