# Terraform Infrastructure-as-Code for Data Lakes
Provision secure cloud data storage structures using Terraform.

```hcl
resource "aws_s3_bucket" "data_lake" {
  bucket = "de-copilot-datalake-prod-2026"
  tags = {
    Environment = "Prod"
    Component   = "DataLake"
  }
}
```
