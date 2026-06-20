# ACID Transactions with Delta Lake in Spark
Maintain consistency in Lakehouse architectures using Delta Lake.

```python
# Write as delta table
df.write.format("delta").mode("overwrite").save("/mnt/delta/customers")
```
