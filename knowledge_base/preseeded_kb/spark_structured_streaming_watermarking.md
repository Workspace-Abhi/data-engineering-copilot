# Watermarking in Spark Structured Streaming
Handle late data and clear states inside event-time windows.

```python
df.withWatermark("event_time", "10 minutes")   .groupBy(window("event_time", "5 minutes"))   .count()
```
