# dbt (Data Build Tool) Blueprint Guide - Part 2

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 4: Project mesh setups in dbt-Databricks adapter
When implementing `Project mesh setups` within a `dbt-Databricks adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement snapshot strategy using check column comparison to log row histories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 5: Custom schema tests in dbt-BigQuery adapter
When implementing `Custom schema tests` within a `dbt-BigQuery adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure sources declarations to track external dependencies and enable source-freshness tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 6: Compile documentation in dbt-Postgres adapter
When implementing `Compile documentation` within a `dbt-Postgres adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use package management hubs to import utility macros like dbt_utils.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

