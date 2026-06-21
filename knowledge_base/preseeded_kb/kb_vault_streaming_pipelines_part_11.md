# Streaming Pipelines Blueprint Guide - Part 11

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 31: Spark Streaming in Apache Kafka Broker
When implementing `Spark Streaming` within a `Apache Kafka Broker` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Integrate Kafka Schema Registry to validate Avro schemas and detect schema breaks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 32: Kafka Schema Registry in Apache Flink Engine
When implementing `Kafka Schema Registry` within a `Apache Flink Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Implement watermarking thresholds in streaming window queries to discard late-arriving events.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 33: Flink DDL setup in Spark Structured Streaming
When implementing `Flink DDL setup` within a `Spark Structured Streaming` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Use stateful deduplication logic utilizing key identifiers to reject duplicate payloads.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

