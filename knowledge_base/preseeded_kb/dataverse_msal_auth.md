# Microsoft Dataverse Integration via MSAL Python & OData Web API

This guide details Python authentication patterns and ingestion scripts to write raw data structures into Microsoft Dataverse entities using Microsoft Authentication Library (MSAL).

---

## 1. OAuth MSAL Client Credentials Authentication

To run automated ETL pipelines, configure a Dataverse App Registration using client credentials grant.

### Python Token Acquisition Setup
```python
from msal import ConfidentialClientApplication
import requests
import json

def get_dataverse_token(tenant_id, client_id, client_secret, resource_url):
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    
    # Initialize MSAL confidential client
    app = ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_secret=client_secret
    )
    
    # Acquire token for tenant
    scopes = [f"{resource_url}/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Token acquisition failed: {result.get('error_description')}")
```

---

## 2. Ingesting Data via OData API (Upsert Payload)

Ingest rows using PATCH operations with Alternate Keys (`cr234_customerid`) to support upserts without query overhead.

### Dataverse Upsert Execution Pattern
```python
def upsert_customer(access_token, resource_url, customer_id, payload):
    # API Headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": "return=representation" -- Returns the updated record
    }
    
    # Entity URL using Alternate Key mapping
    url = f"{resource_url}/api/data/v9.2/cr234_customers(cr234_customerid='{customer_id}')"
    
    response = requests.patch(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )
    return response.status_code, response.json()
```

---

## 3. Dataverse OptionSet Choice Code Values

When updating Choice (OptionSet) fields in Dataverse, payload values must use their internal numeric representations rather than display texts.

### Mapping Schema Examples
- **Status Options**:
  - `Active` ➔ `841200000`
  - `Inactive` ➔ `841200001`
  - `Suspended` ➔ `841200002`

### Choice Value Ingestion Payload
```json
{
  "cr234_name": "Acme Corp",
  "cr234_email": "billing@acme.com",
  "cr234_statuscode": 841200000
}
```
