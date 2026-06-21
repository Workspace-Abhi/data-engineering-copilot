# Streaming Pipelines Blueprint Guide - Part 16

This documentation blueprint details core rules, best practices, and recipes for `Streaming Pipelines` operations.

### Pattern 46: Event time windows in Confluent Cloud Registry
When implementing `Event time windows` within a `Confluent Cloud Registry` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Utilize sliding event time windows to aggregate metrics over continuous intervals.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 47: Slide windows in Azure Event Hubs
When implementing `Slide windows` within a `Azure Event Hubs` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Design partition keys carefully to distribute traffic uniformly across Kafka brokers.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.
---### Pattern 48: Watermarking offsets in AWS Kinesis Engine
When implementing `Watermarking offsets` within a `AWS Kinesis Engine` environment, the core engineering principle dictates the following approach:
*   **Best Practice**: Leverage Flink DDL to directly connect stream sources to target analytics sinks.
*   **Rationale**: This ensures optimal performance metrics, avoids standard anti-patterns, and supports high-volume operations.
*   **Detailed Guideline**: Data engineers should verify configuration properties and trace pipeline logs to confirm implementation success.

