# Event Stream Deduplication in Apache Kafka
Handle duplicate events in high-throughput Kafka topics.

## Approaches
- **Idempotent Producers**: Set `enable.idempotence=true` to prevent duplicates from network retries.
- **Transactional Writes**: Use Kafka Transactions for exactly-once semantics.
- **Stateful Deduplication**: Filter messages inside Spark Streaming using a state store.
