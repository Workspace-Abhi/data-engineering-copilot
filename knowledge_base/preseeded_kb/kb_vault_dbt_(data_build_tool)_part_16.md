# dbt (Data Build Tool) Blueprint Guide - Part 16

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 46: Compile documentation in dbt-Databricks adapter
When implementing `Compile documentation` within a `dbt-Databricks adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use package management hubs to import utility macros like dbt_utils.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 47: Macro functions in dbt-BigQuery adapter
When implementing `Macro functions` within a `dbt-BigQuery adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build reusable custom macros utilizing Jinja syntax for repetitive filter queries.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 48: Package imports in dbt-Postgres adapter
When implementing `Package imports` within a `dbt-Postgres adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Document tables and columns inline in schema files to auto-compile data catalogs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

