# dbt (Data Build Tool) Blueprint Guide - Part 15

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 43: Snapshot strategies in dbt Core Engine
When implementing `Snapshot strategies` within a `dbt Core Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use the ref() function instead of hardcoding database names to build dynamic lineages.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 44: Project mesh setups in dbt Cloud Service
When implementing `Project mesh setups` within a `dbt Cloud Service` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement snapshot strategy using check column comparison to log row histories.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 45: Custom schema tests in dbt-Snowflake adapter
When implementing `Custom schema tests` within a `dbt-Snowflake adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure sources declarations to track external dependencies and enable source-freshness tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

