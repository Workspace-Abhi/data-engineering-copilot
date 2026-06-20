# Tuning Executor Memory and Garbage Collection in Spark
Fine-tune executor settings to prevent Out-Of-Memory (OOM) failures.

- Set `spark.memory.fraction` and `spark.memory.storageFraction`.
- Switch to G1GC garbage collector.
