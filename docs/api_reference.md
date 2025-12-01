# API Reference

## Agents

### `create_policy_extractor_agent`
```python
def create_policy_extractor_agent(
    retry_config: types.HttpRetryOptions
) -> LlmAgent
```

Creates an agent that extracts compliance requirements from policy documents.

**Parameters:**
- `retry_config` (HttpRetryOptions): Retry configuration for API calls

**Returns:**
- `LlmAgent`: Configured policy extraction agent

**Example:**
```python
from src.agents import create_policy_extractor_agent
from src.utils.config import get_retry_config

retry_config = get_retry_config()
agent = create_policy_extractor_agent(retry_config)
```

---

### `create_document_scanner_agent`
```python
def create_document_scanner_agent(
    retry_config: types.HttpRetryOptions
) -> LlmAgent
```

Creates an agent that scans documents for compliance violations.

**Parameters:**
- `retry_config` (HttpRetryOptions): Retry configuration for API calls

**Returns:**
- `LlmAgent`: Configured document scanner agent

**Example:**
```python
from src.agents import create_document_scanner_agent

agent = create_document_scanner_agent(retry_config)
```

---

### `create_violation_analyzer_agent`
```python
def create_violation_analyzer_agent(
    retry_config: types.HttpRetryOptions
) -> LlmAgent
```

Creates an agent that analyzes violations and assigns severity scores.

**Parameters:**
- `retry_config` (HttpRetryOptions): Retry configuration for API calls

**Returns:**
- `LlmAgent`: Configured violation analyzer agent

---

### `create_rewrite_agent`
```python
def create_rewrite_agent(
    retry_config: types.HttpRetryOptions
) -> LlmAgent
```

Creates an agent that generates compliant rewrites.

**Parameters:**
- `retry_config` (HttpRetryOptions): Retry configuration for API calls

**Returns:**
- `LlmAgent`: Configured rewrite agent

---

### `create_orchestrator_agent`
```python
def create_orchestrator_agent(
    policy_extractor: LlmAgent,
    document_scanner: LlmAgent,
    violation_analyzer: LlmAgent,
    rewrite_agent: LlmAgent,
    retry_config: types.HttpRetryOptions
) -> LlmAgent
```

Creates the orchestrator agent that coordinates the workflow.

**Parameters:**
- `policy_extractor` (LlmAgent): Policy extraction agent
- `document_scanner` (LlmAgent): Document scanner agent
- `violation_analyzer` (LlmAgent): Violation analyzer agent
- `rewrite_agent` (LlmAgent): Rewrite agent
- `retry_config` (HttpRetryOptions): Retry configuration

**Returns:**
- `LlmAgent`: Configured orchestrator agent

**Example:**
```python
from src.agents import (
    create_orchestrator_agent,
    create_policy_extractor_agent,
    # ... other agents
)

orchestrator = create_orchestrator_agent(
    policy_extractor,
    document_scanner,
    violation_analyzer,
    rewrite_agent,
    retry_config
)
```

---

## Tools

### `extract_text_from_pdf`
```python
def extract_text_from_pdf(pdf_content: bytes) -> Dict[str, Any]
```

Extracts text from PDF file.

**Parameters:**
- `pdf_content` (bytes): PDF file content as bytes

**Returns:**
- `dict`: Result dictionary with keys:
  - `status` (str): "success" or "error"
  - `text` (str): Extracted text (if successful)
  - `page_count` (int): Number of pages (if successful)
  - `error_message` (str): Error details (if failed)

**Example:**
```python
from src.tools.pdf_ingestion import extract_text_from_pdf

with open("policy.pdf", "rb") as f:
    pdf_bytes = f.read()

result = extract_text_from_pdf(pdf_bytes)
if result["status"] == "success":
    print(f"Extracted {result['page_count']} pages")
    print(result["text"])
```

---

### `parse_policy_structure`
```python
def parse_policy_structure(policy_text: str) -> Dict[str, Any]
```

Parses policy text into structured sections.

**Parameters:**
- `policy_text` (str): Raw policy document text

**Returns:**
- `dict`: Parsed structure with keys:
  - `status` (str): "success" or "error"
  - `sections` (dict): Dictionary of section names to content
  - `total_sections` (int): Number of sections found

---

### `parse_compliance_response`
```python
def parse_compliance_response(response_text: str) -> Dict[str, Any]
```

Parses agent response to extract violation counts and metrics.

**Parameters:**
- `response_text` (str): Raw agent response text

**Returns:**
- `dict`: Parsed results with keys:
  - `violations` (dict): Violations by severity level
  - `total_violations` (int): Total violation count
  - `severity_counts` (dict): Count per severity level
  - `rewrites_generated` (int): Number of rewrites found

**Example:**
```python
from src.tools.response_parser import parse_compliance_response

response = """
🔴 CRITICAL: 2
🟠 HIGH: 3
✅ COMPLIANT REWRITE: ...
"""

result = parse_compliance_response(response)
print(f"Total violations: {result['total_violations']}")
print(f"Rewrites: {result['rewrites_generated']}")
```

---

## Utilities

### `get_retry_config`
```python
def get_retry_config(
    attempts: int = 5,
    exp_base: int = 7,
    initial_delay: int = 1,
    http_status_codes: Optional[List[int]] = None
) -> types.HttpRetryOptions
```

Creates retry configuration for API calls.

**Parameters:**
- `attempts` (int): Maximum retry attempts (default: 5)
- `exp_base` (int): Exponential backoff base (default: 7)
- `initial_delay` (int): Initial delay in seconds (default: 1)
- `http_status_codes` (List[int]): Status codes to retry (default: [429, 500, 503, 504])

**Returns:**
- `HttpRetryOptions`: Configured retry options

---

### `load_api_key`
```python
def load_api_key() -> str
```

Loads Google API key from environment.

**Returns:**
- `str`: API key

**Raises:**
- `ValueError`: If API key not found

**Example:**
```python
import os
from src.utils.config import load_api_key

# Set environment variable first
os.environ["GOOGLE_API_KEY"] = "your-key"

api_key = load_api_key()
```

---

## Complete Example
```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agents import (
    create_orchestrator_agent,
    create_policy_extractor_agent,
    create_document_scanner_agent,
    create_violation_analyzer_agent,
    create_rewrite_agent,
)
from src.utils.config import get_retry_config, load_api_key
from src.tools.response_parser import parse_compliance_response


async def main():
    # Setup
    load_api_key()
    retry_config = get_retry_config()
    
    # Create agents
    policy_extractor = create_policy_extractor_agent(retry_config)
    document_scanner = create_document_scanner_agent(retry_config)
    violation_analyzer = create_violation_analyzer_agent(retry_config)
    rewrite_agent = create_rewrite_agent(retry_config)
    
    orchestrator = create_orchestrator_agent(
        policy_extractor,
        document_scanner,
        violation_analyzer,
        rewrite_agent,
        retry_config
    )
    
    # Setup runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator,
        app_name="ComplianceDemo",
        session_service=session_service
    )
    
    # Load documents
    with open("demo_data/acme_corporation_company_policy.txt") as f:
        policy = f.read()
    
    with open("demo_data/acme_doc_to_scan_proposal_for_new_feature.txt") as f:
        document = f.read()
    
    # Run compliance check
    query = f"Check this document against policy:\n\nPOLICY:\n{policy}\n\nDOCUMENT:\n{document}"
    
    query_content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    response_text = ""
    async for event in runner.run_async(
        user_id="demo",
        session_id="demo_001",
        new_message=query_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text'):
                    response_text += part.text
    
    # Parse results
    results = parse_compliance_response(response_text)
    print(f"Violations found: {results['total_violations']}")
    print(f"Severity breakdown: {results['severity_counts']}")


if __name__ == "__main__":
    asyncio.run(main())
```