# Apache Airflow Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 19: Custom operators in Airflow 2.8+ Engine
When implementing `Custom operators` within a `Airflow 2.8+ Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set default_args dict with retries=3 and backoff_factor to handle transient errors.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Connection pools in Astronomer Astro Core
When implementing `Connection pools` within a `Astronomer Astro Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use DockerOperator or KubernetesPodOperator to isolate execution environment dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: DAG Topologies in MWAA AWS Airflow
When implementing `DAG Topologies` within a `MWAA AWS Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use TaskGroups to modularize task diagrams and simplify web console rendering.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

