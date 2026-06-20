# Provisioning Snowflake Infrastructure with Terraform
Deploy databases, roles, and warehouses dynamically.

```hcl
resource "snowflake_database" "db" {
  name = "RAW_DATA"
}
```
