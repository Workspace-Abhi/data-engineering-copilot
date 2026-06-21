# Streaming Pipelines Blueprint Guide - Part 7

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 19: Partition keys selection in Apache Kafka Broker
When implementing `Partition keys selection` within a `Apache Kafka Broker` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure buffer size thresholds to prevent out-of-memory errors on high-throughput runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 20: Consumer group offsets in Apache Flink Engine
When implementing `Consumer group offsets` within a `Apache Flink Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Monitor consumer lag using Prometheus metrics to scale partition allocations.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 21: Spark Streaming in Spark Structured Streaming
When implementing `Spark Streaming` within a `Spark Structured Streaming` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Integrate Kafka Schema Registry to validate Avro schemas and detect schema breaks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

