# testing and Documentation in dbt
Implement rigorous testing pipelines using dbt Core.

## Schema Tests
Specify tests inside your `schema.yml` file:
- `unique`: Verifies if a column only contains unique values.
- `not_null`: Verifies if there are no null records.
- `accepted_values`: Restricts values to a specific list.

```yaml
version: 2
models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
```
