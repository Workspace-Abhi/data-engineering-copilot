# Streaming Pipelines Blueprint Guide - Part 9

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 25: Checkpoint stores in Apache Kafka Broker
When implementing `Checkpoint stores` within a `Apache Kafka Broker` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Optimize consumer group offset committing intervals to reduce replication lags.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 26: Event time windows in Apache Flink Engine
When implementing `Event time windows` within a `Apache Flink Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize sliding event time windows to aggregate metrics over continuous intervals.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 27: Slide windows in Spark Structured Streaming
When implementing `Slide windows` within a `Spark Structured Streaming` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Design partition keys carefully to distribute traffic uniformly across Kafka brokers.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

