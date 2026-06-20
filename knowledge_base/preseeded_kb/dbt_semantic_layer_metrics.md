# Implementing dbt Semantic Layer Metrics
Define consistent calculations (metrics) for BI tools inside dbt models.

```yaml
semantic_models:
  - name: orders
    measures:
      - name: order_total
        agg: sum
```
