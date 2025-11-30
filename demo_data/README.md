# Demo Data

This directory contains sample policies, documents, and test data for the Compliance Copilot.

## Files

- **sample_policy.txt**: Sample company data security policy
- **sample_document.txt**: Sample feature proposal with violations
- **test_documents/**: Test corpus with labeled violations
- **gold_labels.json**: Ground truth labels for evaluation

## Test Documents

| File | Description | Violations |
|------|-------------|------------|
| doc_001_critical.txt | Critical security issues | 4 CRITICAL |
| doc_002_high.txt | High-risk violations | 4 HIGH |
| doc_003_medium.txt | Medium-risk issues | 2 MEDIUM |
| doc_004_mixed.txt | Mixed severity | 3 CRITICAL, 1 HIGH |
| doc_005_clean.txt | Compliant document | 0 |

## Usage

### In Kaggle

1. Upload this folder as a dataset
2. Add to notebook as input
3. Reference files at `/kaggle/input/compliance-test-data/`

### Locally
```python
from pathlib import Path

# Load sample policy
with open("demo_data/sample_policy.txt", "r") as f:
    policy = f.read()

# Load test document
with open("demo_data/sample_document.txt", "r") as f:
    document = f.read()
```