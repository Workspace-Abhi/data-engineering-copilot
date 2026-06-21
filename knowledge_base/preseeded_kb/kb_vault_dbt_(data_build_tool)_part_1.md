# dbt (Data Build Tool) Blueprint Guide - Part 1

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 1: Staging configurations in dbt Core Engine
When implementing `Staging configurations` within a `dbt Core Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure incremental models using merge strategy on Snowflake and Databricks platforms.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 2: Incremental strategies in dbt Cloud Service
When implementing `Incremental strategies` within a `dbt Cloud Service` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Write custom schema validation tests inside schema.yml files to verify business keys.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 3: Snapshot strategies in dbt-Snowflake adapter
When implementing `Snapshot strategies` within a `dbt-Snowflake adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use the ref() function instead of hardcoding database names to build dynamic lineages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

