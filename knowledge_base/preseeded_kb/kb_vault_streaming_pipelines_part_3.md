# Streaming Pipelines Blueprint Guide - Part 3

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 7: Slide windows in Apache Kafka Broker
When implementing `Slide windows` within a `Apache Kafka Broker` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Design partition keys carefully to distribute traffic uniformly across Kafka brokers.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 8: Watermarking offsets in Apache Flink Engine
When implementing `Watermarking offsets` within a `Apache Flink Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Flink DDL to directly connect stream sources to target analytics sinks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 9: Partition keys selection in Spark Structured Streaming
When implementing `Partition keys selection` within a `Spark Structured Streaming` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Configure buffer size thresholds to prevent out-of-memory errors on high-throughput runs.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

