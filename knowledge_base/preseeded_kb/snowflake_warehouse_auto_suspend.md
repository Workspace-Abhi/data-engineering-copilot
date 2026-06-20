# Snowflake Warehouse Auto-Suspend and Scaling
Optimize Snowflake costs by adjusting virtual warehouses.

```sql
ALTER WAREHOUSE COMPUTE_WH SET 
  AUTO_SUSPEND = 60 
  AUTO_RESUME = TRUE 
  MIN_CLUSTER_COUNT = 1 
  MAX_CLUSTER_COUNT = 5;
```
