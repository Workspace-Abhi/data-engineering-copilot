# Apache Airflow Blueprint Guide - Part 1

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 1: DAG Topologies in Airflow 2.8+ Engine
When implementing `DAG Topologies` within a `Airflow 2.8+ Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use TaskGroups to modularize task diagrams and simplify web console rendering.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 2: TaskGroups in Astronomer Astro Core
When implementing `TaskGroups` within a `Astronomer Astro Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement poke-mode sensors with custom timeout limits to prevent task slot starvation.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 3: Sensors in MWAA AWS Airflow
When implementing `Sensors` within a `MWAA AWS Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use dynamic task mapping with expand() to process variable datasets dynamically.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

