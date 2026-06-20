# PySpark Query Optimization on Databricks
Learn how to optimize slow PySpark executions on Databricks clusters.

## Common Strategies
1. **Adaptive Query Execution (AQE)**: Automatically optimizes query plans during runtime.
2. **Broadcast Joins**: Use broadcasting for small lookup tables (<10MB by default) to avoid shuffles.
3. **Partition Pruning**: Filter rows based on partition keys to minimize input scan size.

```python
# Force broadcast join
from pyspark.sql.functions import broadcast

optimized_df = large_df.join(broadcast(small_df), "join_key")
```
