"""API Integration Agent for generating ingestion patterns, webhook handlers, and rate limiting."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("api_integration_agent")

class ApiIntegrationAgent:
    """Specialized agent for API ingestion and webhook integration patterns."""

    SYSTEM_PROMPT = """You are an expert Data Integration and API Engineer. You specialize in:
- Building REST API extraction scripts with pagination, retries, and rate-limiting
- Designing webhook endpoints and message parsing logic
- Configuring authorization patterns (OAuth2 client credentials, API keys)
- Processing streaming feeds and JSON payload schema flattening

Always provide clean Python code using standard libraries (requests, urllib3) or FastAPI."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process an API integration related query."""
        rag_context = self.rag_service.get_context(query, k=3)
        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with API extraction or webhook handler examples where applicable."""

        return self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

    def generate_rest_ingestion(self, url: str, auth_type: str = "Bearer") -> str:
        """Generate a Python requests ingestion template with rate limiting and pagination."""
        code = f"""import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def get_api_client():
    session = requests.Session()
    # Configure retry logic for transient errors (rate limit 429, gateway 502/503/504)
    retries = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_paginated_data():
    client = get_api_client()
    url = "{url}"
    headers = {{
        "Authorization": "{auth_type} YOUR_TOKEN_HERE",
        "Accept": "application/json"
    }}
    
    params = {{"page": 1, "per_page": 100}}
    all_records = []
    
    while True:
        print(f"Fetching page {{params['page']}}...")
        response = client.get(url, headers=headers, params=params, timeout=30)
        
        # Enforce rate limits (cooldown) if header exists
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"Rate limited. Sleeping for {{retry_after}} seconds...")
            time.sleep(retry_after)
            continue
            
        response.raise_for_status()
        data = response.json()
        
        if not data or len(data) == 0:
            break
            
        all_records.extend(data)
        params["page"] += 1
        
        # Micro-sleep to respect standard API consumption rate
        time.sleep(0.2)
        
    return all_records
"""
        return code

    def generate_webhook_handler(self) -> str:
        """Generate a FastAPI webhook receiver with verification."""
        code = """from fastapi import FastAPI, Header, HTTPException, Request
import hmac
import hashlib

app = FastAPI()
WEBHOOK_SECRET = b"your_secret_key"

@app.post("/webhook/v1/ingest")
async def receive_webhook(request: Request, x_signature: str = Header(None)):
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing signature header")
        
    body = await request.body()
    
    # Verify SHA256 HMAC signature to validate authenticity
    expected_sig = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(f"sha256={expected_sig}", x_signature):
        raise HTTPException(status_code=403, detail="Invalid signature verification failed")
        
    payload = await request.json()
    print("Signature Verified! Processing webhook payload...")
    
    # Process event asynchronously
    return {"status": "accepted", "event_id": payload.get("id")}
"""
        return code


def get_api_integration_agent() -> ApiIntegrationAgent:
    """Get API Integration agent instance."""
    return ApiIntegrationAgent()
