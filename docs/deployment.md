# Deployment Guide

## Overview

This guide covers deploying the AI Enterprise Compliance Copilot in various environments.

## Prerequisites

- Python 3.11+
- Google API Key with Gemini API access
- 4GB+ RAM recommended
- Internet connection for API calls

## Local Deployment

### 1. Setup
```bash
# Clone repository
git clone https://github.com/yourusername/ai-compliance-copilot.git
cd ai-compliance-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Option 1: Environment variable
export GOOGLE_API_KEY="your-api-key-here"

# Option 2: .env file
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

### 3. Run
```bash
# Single document check
python scripts/run_evaluation.py \
  --policy demo_data/acme_corporation_company_policy.txt \
  --document demo_data/acme_doc_to_scan_proposal_for_new_feature.txt

# Full evaluation
python tests/evaluation.py
```

## Kaggle Deployment

### 1. Create Dataset

1. Go to Kaggle → Datasets → New Dataset
2. Upload `demo_data/` folder
3. Name: `compliance-test-data`
4. Set visibility (public/private)

### 2. Setup Notebook

1. Upload `notebooks/demo_compliance_agent.ipynb`
2. Add dataset in "Input" section
3. Add `GOOGLE_API_KEY` to Secrets:
   - Click "Add-ons" → "Secrets"
   - Add secret: `GOOGLE_API_KEY`
   - Paste your API key

### 3. Run

Click "Run All" in Kaggle notebook.

## Cloud Deployment

### Google Cloud Run
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/run_evaluation.py", "--policy", "demo_data/acme_corporation_company_policy.txt", "--document", "demo_data/acme_doc_to_scan_proposal_for_new_feature.txt"]
EOF

# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/compliance-copilot
gcloud run deploy compliance-copilot \
  --image gcr.io/PROJECT_ID/compliance-copilot \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=your-api-key-here
```

### AWS Lambda
```bash
# Create deployment package
pip install -r requirements.txt -t package/
cp -r src/ package/
cd package && zip -r ../deployment.zip . && cd ..

# Upload to Lambda
aws lambda create-function \
  --function-name ComplianceCopilot \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment.zip \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
  --environment Variables="{GOOGLE_API_KEY=your-api-key-here}"
```

## Production Considerations

### Rate Limits

Gemini 2.0 Flash Lite free tier limits:
- 15 requests per minute
- 1 million tokens per minute

For production:
- Implement request queuing
- Add caching for repeated policy extractions
- Consider paid tier for higher limits

### Security

**API Key Protection:**
```python
# Use secret management
from google.cloud import secretmanager

def get_api_key():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/PROJECT/secrets/google-api-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

**Input Validation:**
```python
def validate_input(text: str, max_length: int = 100000):
    if len(text) > max_length:
        raise ValueError(f"Input exceeds {max_length} characters")
    if not text.strip():
        raise ValueError("Input cannot be empty")
```

### Monitoring

**Add logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('compliance_copilot.log'),
        logging.StreamHandler()
    ]
)
```

**Track metrics:**
```python
from prometheus_client import Counter, Histogram

violations_found = Counter('violations_found', 'Total violations detected')
processing_time = Histogram('processing_time', 'Document processing time')
```

### Scaling

**Horizontal Scaling:**
- Agents are stateless (can run in parallel)
- Use message queue (RabbitMQ, Cloud Tasks) for batch processing
- Deploy multiple instances behind load balancer

**Batch Processing:**
```python
async def process_batch(documents: List[str]):
    tasks = [run_compliance_check(doc) for doc in documents]
    results = await asyncio.gather(*tasks)
    return results
```

## Cost Estimation

### API Costs (Gemini 2.0 Flash Lite)

Free tier: Up to 1500 requests/day
- Input: $0.075 / 1M tokens
- Output: $0.30 / 1M tokens

Average document (5000 tokens input + 2000 output):
- Cost per document: ~$0.001
- 1000 documents/day: ~$1/day

### Infrastructure Costs

- **Kaggle**: Free (public notebooks)
- **Cloud Run**: ~$0.01/hour when running
- **Lambda**: ~$0.20/1M requests
- **Compute Engine**: ~$50/month (e2-medium)

## Troubleshooting

### Common Issues

**1. Rate Limit Exceeded**
```python
# Solution: Implement retry with exponential backoff
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429]
)
```

**2. Out of Memory**
```python
# Solution: Process in chunks
def chunk_text(text: str, chunk_size: int = 10000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

**3. Slow Processing**
```python
# Solution: Use faster model or parallel processing
model = Gemini(model="gemini-2.0-flash-lite")  # Faster than Pro
```

## Support

For issues:
- GitHub Issues: https://github.com/yourusername/ai-compliance-copilot/issues
- Email: pratik.clin@gmail.com