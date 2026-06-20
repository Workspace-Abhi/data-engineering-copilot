# Deploying Google Cloud Composer with Terraform
Create fully managed Airflow environments in GCP.

```hcl
resource "google_composer_environment" "env" {
  name   = "de-composer-environment"
  region = "us-central1"
}
```
