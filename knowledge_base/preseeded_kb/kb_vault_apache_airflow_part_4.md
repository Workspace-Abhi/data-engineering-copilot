# Apache Airflow Blueprint Guide - Part 4

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 10: Connection pools in Composer GCP Airflow
When implementing `Connection pools` within a `Composer GCP Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use DockerOperator or KubernetesPodOperator to isolate execution environment dependencies.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 11: DAG Topologies in Airflow Local Localhost
When implementing `DAG Topologies` within a `Airflow Local Localhost` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use TaskGroups to modularize task diagrams and simplify web console rendering.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 12: TaskGroups in Celery Executor Backend
When implementing `TaskGroups` within a `Celery Executor Backend` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement poke-mode sensors with custom timeout limits to prevent task slot starvation.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

