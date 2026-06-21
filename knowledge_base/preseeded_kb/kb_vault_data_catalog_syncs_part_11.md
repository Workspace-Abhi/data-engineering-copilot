# Data Catalog Syncs Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Data Catalog Syncs` operations.

### Pattern 31: Metadata extraction configs in Collibra API Catalog
When implementing `Metadata extraction configs` within a `Collibra API Catalog` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure metadata extraction tasks to auto-extract data schemas from databases daily.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Data dictionaries MD in Apache Atlas Metadata
When implementing `Data dictionaries MD` within a `Apache Atlas Metadata` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Publish data dictionaries in markdown format to build repository search directories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Lineage traversers in Azure Purview API
When implementing `Lineage traversers` within a `Azure Purview API` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Enable OpenLineage integrations in Spark to trace parent-child table linkages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

