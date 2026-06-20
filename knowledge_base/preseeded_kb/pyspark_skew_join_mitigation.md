# Mitigating Skew Joins in Apache Spark
Avoid partitions that bottleneck execution due to unbalanced join keys.

- **Salting**: Append a random integer suffix to join keys to distribute data.
- **AQE Skew Join**: AQE splits skewed partitions automatically.
