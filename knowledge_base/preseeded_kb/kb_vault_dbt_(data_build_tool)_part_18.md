# dbt (Data Build Tool) Blueprint Guide - Part 18

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 52: Incremental strategies in dbt-Databricks adapter
When implementing `Incremental strategies` within a `dbt-Databricks adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write custom schema validation tests inside schema.yml files to verify business keys.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 53: Snapshot strategies in dbt-BigQuery adapter
When implementing `Snapshot strategies` within a `dbt-BigQuery adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use the ref() function instead of hardcoding database names to build dynamic lineages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 54: Project mesh setups in dbt-Postgres adapter
When implementing `Project mesh setups` within a `dbt-Postgres adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement snapshot strategy using check column comparison to log row histories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

