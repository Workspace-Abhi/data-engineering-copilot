# dbt (Data Build Tool) Blueprint Guide - Part 19

This documentation blueprint details core rules, best practices, and recipes for `dbt (Data Build Tool)` operations.

### Pattern 55: Custom schema tests in dbt Core Engine
When implementing `Custom schema tests` within a `dbt Core Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure sources declarations to track external dependencies and enable source-freshness tests.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 56: Compile documentation in dbt Cloud Service
When implementing `Compile documentation` within a `dbt Cloud Service` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use package management hubs to import utility macros like dbt_utils.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 57: Macro functions in dbt-Snowflake adapter
When implementing `Macro functions` within a `dbt-Snowflake adapter` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Build reusable custom macros utilizing Jinja syntax for repetitive filter queries.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

