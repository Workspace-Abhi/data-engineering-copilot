# Data Validation with Great Expectations
Set up automated quality checks in python pipelines.

```python
import great_expectations as ge

df = ge.read_csv("data.csv")
df.expect_column_values_to_not_be_null("customer_id")
df.expect_column_unique_value_count_to_be_between("status", 2, 5)
```
