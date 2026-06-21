# Apache Airflow Blueprint Guide - Part 15

This documentation blueprint details core rules, best practices, and recipes for `Apache Airflow` operations.

### Pattern 43: Sensors in Airflow 2.8+ Engine
When implementing `Sensors` within a `Airflow 2.8+ Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use dynamic task mapping with expand() to process variable datasets dynamically.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 44: Dynamic mapping in Astronomer Astro Core
When implementing `Dynamic mapping` within a `Astronomer Astro Core` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure custom XCom backend utilizing ADLS or S3 to store large metadata files.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 45: XCom backend in MWAA AWS Airflow
When implementing `XCom backend` within a `MWAA AWS Airflow` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Set DAG-level concurrency limit to prevent resource depletion of task worker pools.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

