# Repository Structure Documentation

**Project:** AI Enterprise Compliance Copilot  
**Version:** 1.0.0  
**Last Updated:** December 1, 2025

---

## 📋 Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Directory Structure](#directory-structure)
3. [Module Organization](#module-organization)
4. [Data Flow](#data-flow)
5. [File Descriptions](#file-descriptions)
6. [Dependencies](#dependencies)
7. [Execution Flow](#execution-flow)

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE COPILOT SYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ORCHESTRATOR AGENT (Coordinator)             │  │
│  │  - Manages workflow sequencing (Steps 1-5)               │  │
│  │  - Routes between specialized agents                     │  │
│  │  - Compiles final compliance report                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌─────────────┬──────────────┬──────────────┬─────────────┐   │
│  │             │              │              │             │   │
│  ▼             ▼              ▼              ▼             ▼   │
│ ┌──────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐      │
│ │ POLICY   │ │ DOCUMENT   │ │ VIOLATION  │ │ REWRITE  │      │
│ │EXTRACTOR │ │ SCANNER    │ │ ANALYZER   │ │ AGENT    │      │
│ │ AGENT    │ │ AGENT      │ │ AGENT      │ │          │      │
│ └──────────┘ └────────────┘ └────────────┘ └──────────┘      │
│                                                                 │
│  TOOLS & UTILITIES LAYER:                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • PDF Ingestion (extract_text_from_pdf)                │   │
│  │ • Response Parser (parse_compliance_response)           │   │
│  │ • Config & Retry Logic (get_retry_config)              │   │
│  │ • Export Tools (JSON, CSV, HTML, PDF)                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  INFRASTRUCTURE:                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • Google ADK (Agent Development Kit)                   │   │
│  │ • Gemini 2.0 Flash Lite (LLM)                         │   │
│  │ • InMemorySessionService (State Management)            │   │
│  │ • Runner + LoggingPlugin (Execution & Observability)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
ai-enterprise-compliance-agent/
├── README.md                              # Project overview & quick start
├── LICENSE                                # MIT License
├── requirements.txt                       # Python dependencies
├── setup.py                               # Package setup configuration
├── CORRECTIONS_APPLIED.md                 # Change log for fixes
├── NOTEBOOK_VALIDATION.md                 # Kaggle notebook validation report
├── REPOSITORY_STRUCTURE.md                # This file
│
├── src/                                   # Main source code
│   ├── __init__.py                        # Package exports
│   │
│   ├── agents/                            # Multi-agent implementations
│   │   ├── __init__.py                    # Agent exports
│   │   ├── orchestrator.py                # Orchestrator (coordinator agent)
│   │   ├── policy_extractor.py            # Policy extraction specialist
│   │   ├── document_scanner.py            # Document scanning specialist
│   │   ├── violation_analyzer.py          # Violation analysis specialist
│   │   └── rewrite_agent.py               # Compliance rewrite specialist
│   │
│   ├── tools/                             # Utility tools & parsers
│   │   ├── __init__.py                    # Tool exports
│   │   ├── pdf_ingestion.py               # PDF text extraction
│   │   └── response_parser.py             # Agent response parsing
│   │
│   ├── exporter/                          # Report export functionality
│   │   ├── __init__.py                    # Exporter exports
│   │   ├── exporter.py                    # Main export orchestrator
│   │   ├── html_template.py               # HTML report template
│   │   └── pdf_generator.py               # PDF generation (reportlab)
│   │
│   └── utils/                             # Configuration & utilities
│       ├── __init__.py                    # Utils exports
│       └── config.py                      # API key loading & retry config
│
├── notebooks/                             # Jupyter notebooks
│   ├── README.md                          # Notebook instructions
│   ├── ai-enterprise-compliance-agent.ipynb  # Main Kaggle notebook
│   └── demo_compliance_agent.ipynb        # Alternative demo notebook
│
├── scripts/                               # Standalone scripts
│   ├── run_evaluation.py                  # Single document evaluation script
│   └── export_results.py                  # Export compliance results to files
│
├── tests/                                 # Test suite
│   ├── __init__.py                        # Test package
│   ├── test_agents.py                     # Agent unit tests
│   ├── test_tools.py                      # Tools unit tests
│   └── evaluation.py                      # Evaluation harness
│
├── docs/                                  # Documentation
│   ├── architecture.md                    # System architecture details
│   ├── deployment.md                      # Deployment guides
│   ├── api_reference.md                   # API reference
│   └── images/                            # Documentation images
│       └── README.md
│
└── demo_data/                             # Sample data for testing
    ├── README.md                          # Demo data description
    ├── acme_corporation_company_policy.txt # Sample policy document
    ├── acme_doc_to_scan_proposal_for_new_feature.txt  # Sample document
    ├── gold_labels.json                   # Ground truth for evaluation
    └── test_documents/                    # Test dataset
        ├── doc_001_critical.txt           # 4 CRITICAL violations
        ├── doc_002_high.txt               # 4 HIGH violations
        ├── doc_003_medium.txt             # 2 MEDIUM violations
        ├── doc_004_mixed.txt              # 3 CRITICAL + 1 HIGH
        └── doc_005_clean.txt              # Compliant document (0 violations)
```

---

## 📦 Module Organization

### 1. **Agents** (`src/agents/`)

The multi-agent system core. Each agent is a specialized LlmAgent with specific instructions.

#### a) **orchestrator.py**
- **Class/Function:** `create_orchestrator_agent()`
- **Purpose:** Coordinates entire compliance workflow
- **Inputs:** All 4 specialist agents + retry config
- **Outputs:** Structured compliance report with violations by severity
- **Workflow:**
  1. Delegates to Policy Extractor
  2. Delegates to Document Scanner (using policies from Step 1)
  3. Delegates to Violation Analyzer for each violation
  4. Delegates to Rewrite Agent for CRITICAL/HIGH violations
  5. Compiles final report
- **Tools:** Wraps all 4 specialist agents as AgentTools
- **Model:** Gemini 2.0 Flash Lite with temperature=0.1 for determinism

#### b) **policy_extractor.py**
- **Class/Function:** `create_policy_extractor_agent()`
- **Purpose:** Extracts compliance requirements from policy documents
- **Input:** Raw policy document text
- **Output:** Structured JSON with rule IDs, categories, requirements, severity levels
- **Key Methods:** Parses policy into actionable rules with metrics
- **Tools:** None (pure text analysis)

#### c) **document_scanner.py**
- **Class/Function:** `create_document_scanner_agent()`
- **Purpose:** Scans documents for violations against extracted policies
- **Input:** Document text + extracted policy requirements
- **Output:** JSON list of potential violations with exact quotes and references
- **Violations Detected:**
  - Hardcoded credentials (passwords, API keys)
  - Unencrypted sensitive data
  - SQL injection vulnerabilities
  - Missing MFA
  - Non-compliant data retention
- **Tools:** None (pure text analysis)

#### d) **violation_analyzer.py**
- **Class/Function:** `create_violation_analyzer_agent()`
- **Purpose:** Analyzes and scores violations by severity
- **Input:** Individual violation + relevant policy requirement
- **Output:** JSON with severity (CRITICAL/HIGH/MEDIUM/LOW), risk analysis, remediation plan, fix time estimate
- **Severity Criteria:**
  - **CRITICAL:** Data breach potential, hardcoded credentials, active vulnerabilities
  - **HIGH:** Missing MFA, SQL injection risks, non-compliant retention
  - **MEDIUM:** Expired keys, incomplete controls
  - **LOW:** Missing labels, documentation issues
- **Tools:** None (pure analysis)

#### e) **rewrite_agent.py**
- **Class/Function:** `create_rewrite_agent()`
- **Purpose:** Generates compliant rewrites for violations
- **Input:** Violating text/code + policy requirement + severity analysis
- **Output:** JSON with original text, compliant version, changes made, compliance achieved
- **Scope:** Generates rewrites only for CRITICAL and HIGH violations
- **Tools:** None (pure text generation)

---

### 2. **Tools** (`src/tools/`)

Shared utility functions for document processing and parsing.

#### a) **pdf_ingestion.py**
- **Functions:**
  - `extract_text_from_pdf(pdf_content: bytes)` → Dict with status, text, page_count
  - `parse_policy_structure(policy_text: str)` → Dict with sections
- **Purpose:** Extract text from PDF files and parse into sections
- **Dependencies:** PyPDF2
- **Output Format:** Dictionary with "status", "text", "page_count" or "error_message"

#### b) **response_parser.py**
- **Functions:**
  - `parse_compliance_response(response_text: str)` → Dict with violations by severity
  - `extract_violation_details(response_text: str)` → List of violation dicts
- **Purpose:** Parse agent responses to extract violations, metrics, and rewrites
- **Regex Patterns:** Handles emoji markers (🔴, 🟠, 🟡, 🟢) and text severities
- **Output:** Structured dictionary with severity breakdown and metrics
- **Handles:**
  - JSON responses with markdown code blocks
  - Text-based severity counts (e.g., "CRITICAL: 2")
  - Rewrite detection and counting

---

### 3. **Exporter** (`src/exporter/`)

Report generation and export functionality.

#### a) **exporter.py**
- **Functions:**
  - `export_to_json(results, output_path)`
  - `export_to_csv(results, output_path)`
  - `export_to_html(results, output_path)`
  - `export_to_pdf(results, output_path)` (requires reportlab)
  - `export_all(results, base_name, output_dir, fmt="all")`
- **Purpose:** Multi-format compliance report export
- **Formats Supported:** JSON, CSV, HTML, PDF, or all
- **Output:** Timestamped files with severity breakdown and violation details

#### b) **html_template.py**
- **Content:** HTML_TEMPLATE string constant
- **Purpose:** Provides HTML template for report rendering
- **Features:** Styled severity badges, summary cards, violation details

#### c) **pdf_generator.py**
- **Functions:** `export_to_pdf(results, output_path)`
- **Purpose:** Generates PDF compliance reports using reportlab
- **Dependencies:** reportlab.lib.pagesizes, reportlab.lib.styles, reportlab.platypus
- **Output:** Professional PDF report with severity breakdown

---

### 4. **Utils** (`src/utils/`)

Configuration and utility functions.

#### a) **config.py**
- **Functions:**
  - `load_api_key()` → str (from environment variable)
  - `get_retry_config(attempts=5, exp_base=7, ...)` → types.HttpRetryOptions
- **Purpose:** API key management and retry logic configuration
- **Retry Strategy:** Exponential backoff (1s → 7s → 49s → 343s)
- **Retryable Status Codes:** [429, 500, 503, 504]

---

## 🔄 Data Flow

### Compliance Check Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ INPUT: Policy Document + Document to Review                      │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: POLICY EXTRACTION                                        │
│ Policy Extractor Agent analyzes policy document                  │
│ Output: {                                                        │
│   "requirements": [                                              │
│     {                                                            │
│       "rule_id": "SEC-1.1",                                     │
│       "category": "Data Security",                              │
│       "requirement": "All PII must be encrypted with AES-256",  │
│       "severity_if_violated": "CRITICAL",                       │
│       "metrics": ["AES-256", "at rest"]                         │
│     }, ...                                                       │
│   ],                                                             │
│   "total_requirements": 15                                       │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: DOCUMENT SCANNING                                        │
│ Document Scanner Agent scans document against requirements       │
│ Output: {                                                        │
│   "violations": [                                                │
│     {                                                            │
│       "violation_id": "V1",                                      │
│       "violating_text": "password = 'Admin123!'",              │
│       "location": "line 42",                                     │
│       "explanation": "Hardcoded password",                       │
│       "violated_rule_id": "SEC-1.2"                             │
│     }, ...                                                       │
│   ],                                                             │
│   "total_violations": 7                                          │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: VIOLATION ANALYSIS (for each violation)                 │
│ Violation Analyzer Agent scores each violation                   │
│ Output: {                                                        │
│   "violation_id": "V1",                                          │
│   "severity": "CRITICAL",                                        │
│   "risk_analysis": {                                             │
│     "security_risk": "High data breach potential",              │
│     "regulatory_impact": "GDPR violation",                       │
│     "business_impact": "Severe reputation damage"               │
│   },                                                             │
│   "remediation_plan": [                                          │
│     "Move to environment variable",                              │
│     "Implement key rotation",                                    │
│     "Add encryption"                                             │
│   ],                                                             │
│   "estimated_fix_time_hours": 2,                                │
│   "priority": 1                                                  │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: GENERATE REWRITES (CRITICAL/HIGH only)                 │
│ Rewrite Agent generates compliant versions                       │
│ Output: {                                                        │
│   "violation_id": "V1",                                          │
│   "original_text": "password = 'Admin123!'",                    │
│   "compliant_rewrite": "password = os.getenv('DB_PASSWORD')",   │
│   "changes_made": [                                              │
│     "Removed hardcoded password",                                │
│     "Added environment variable"                                 │
│   ],                                                             │
│   "compliance_achieved": ["SEC-1.2", "SEC-2.1"]                │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: COMPILE FINAL REPORT                                     │
│ Orchestrator aggregates all results                              │
│ Output: Human-readable compliance report with:                   │
│ • Executive summary (total violations by severity)               │
│ • Severity breakdown with details                                │
│ • All rewrites and remediation plans                             │
│ • Estimated total fix time                                       │
│ • Overall compliance status (PASS/FAIL)                          │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ OUTPUT: Compliance Report                                         │
│ Format: Text / JSON / CSV / HTML / PDF                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📄 File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `README.md` | Project overview, quick start, architecture diagram |
| `setup.py` | Package metadata, dependencies, installation config |
| `requirements.txt` | Python package dependencies with versions |
| `LICENSE` | MIT License text |
| `.gitignore` | Git ignore rules |
| `CORRECTIONS_APPLIED.md` | Record of fixes and improvements made |
| `NOTEBOOK_VALIDATION.md` | Kaggle notebook validation and recommendations |
| `REPOSITORY_STRUCTURE.md` | This file |

### Source Code (`src/`)

**Agents** — Multi-agent implementations for specialized compliance tasks

**Tools** — Reusable utilities for PDF processing and response parsing

**Exporter** — Report generation in multiple formats

**Utils** — Configuration management and retry logic

### Scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| `run_evaluation.py` | CLI to run compliance check on single document |
| `export_results.py` | Export compliance results from JSON to multiple formats |

### Tests (`tests/`)

| File | Purpose |
|------|---------|
| `test_agents.py` | Unit tests for agent creation and configuration |
| `test_tools.py` | Unit tests for PDF ingestion and response parsing |
| `evaluation.py` | Full evaluation harness for test dataset |

### Notebooks (`notebooks/`)

| Notebook | Purpose |
|----------|---------|
| `ai-enterprise-compliance-agent.ipynb` | Main Kaggle demo notebook (41 cells) |
| `demo_compliance_agent.ipynb` | Alternative demo notebook |

### Documentation (`docs/`)

| Doc | Purpose |
|-----|---------|
| `architecture.md` | Detailed system architecture |
| `deployment.md` | Deployment guides (local, Kaggle, Cloud Run, Lambda) |
| `api_reference.md` | API reference for all modules |

### Demo Data (`demo_data/`)

| File | Purpose |
|------|---------|
| `acme_corporation_company_policy.txt` | Sample compliance policy |
| `acme_doc_to_scan_proposal_for_new_feature.txt` | Sample document with violations |
| `gold_labels.json` | Expected violations for evaluation |
| `test_documents/` | 5 test documents with known violation counts |

---

## 🔌 Dependencies

### Core Dependencies

```
google-adk>=0.1.0              # Agent Development Kit
google-generativeai>=0.8.0     # Gemini API
PyPDF2>=3.0.0                  # PDF text extraction
reportlab>=4.0.0               # PDF generation
```

### Development Dependencies

```
pytest>=7.4.0                  # Testing framework
pytest-asyncio>=0.21.0         # Async test support
jupyter>=1.0.0                 # Jupyter notebooks
```

### Utilities

```
python-dotenv>=1.0.0           # Environment variable management
pandas>=1.0.0                  # Data processing (optional)
numpy>=1.0.0                   # Numerical operations (optional)
tqdm>=4.0.0                    # Progress bars (optional)
```

---

## 🚀 Execution Flow

### Local Execution

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
export GOOGLE_API_KEY="your-api-key"

# Single document check
python scripts/run_evaluation.py \
  --policy demo_data/acme_corporation_company_policy.txt \
  --document demo_data/acme_doc_to_scan_proposal_for_new_feature.txt

# Full evaluation
python tests/evaluation.py

# Export results
python scripts/export_results.py \
  --input results.json \
  --format all \
  --output-dir output/
```

### Kaggle Execution

```
1. Upload `demo_data/` as dataset
2. Upload `notebooks/ai-enterprise-compliance-agent.ipynb`
3. Add `GOOGLE_API_KEY` to Kaggle Secrets
4. Run all cells
5. Runtime: ~10-15 minutes
```

### Python API Usage

```python
from src.agents import (
    create_orchestrator_agent,
    create_policy_extractor_agent,
    create_document_scanner_agent,
    create_violation_analyzer_agent,
    create_rewrite_agent,
)
from src.utils.config import get_retry_config

# Initialize
retry_config = get_retry_config()
policy_agent = create_policy_extractor_agent(retry_config)
scanner_agent = create_document_scanner_agent(retry_config)
analyzer_agent = create_violation_analyzer_agent(retry_config)
rewrite_agent = create_rewrite_agent(retry_config)
orchestrator = create_orchestrator_agent(
    policy_agent, scanner_agent, analyzer_agent, rewrite_agent, retry_config
)

# Run compliance check (async)
import asyncio
response = asyncio.run(run_compliance_check(orchestrator, policy_text, document_text))
```

---

## 📊 Key Metrics & Performance

| Metric | Value |
|--------|-------|
| **Time Reduction** | 4 hours → 12 minutes (95%) |
| **Detection Rate** | 75% → 100% (25% improvement) |
| **Precision** | 95.9% |
| **Recall** | 100% (zero false negatives) |
| **F1 Score** | 0.979 |
| **Cost Reduction** | $200 → $5 per review (97.5%) |
| **Agents** | 5 (1 orchestrator + 4 specialists) |
| **Throughput** | 40 docs/day vs 2 manual |

---

## 🔐 Security & Best Practices

### API Key Management
- Stored in environment variables, not in code
- Loaded via `src/utils/config.py::load_api_key()`
- Kaggle Secrets integration for notebooks

### Retry Logic
- Exponential backoff for rate limits
- Configurable retry attempts (default: 5)
- Status codes: 429, 500, 503, 504

### Error Handling
- PDF extraction failures → graceful fallback
- Missing API key → clear error message
- Invalid JSON responses → text-based parsing fallback

### Input Validation
- Policy document length limits
- Document text encoding handling
- Violation ID uniqueness checks

---

## 📈 Scalability & Deployment

### Horizontal Scaling
- Stateless agents (can run in parallel)
- Session-based memory (isolated per user)
- No shared state between agent instances

### Cloud Deployment Options
1. **Kaggle** - Free, public/private notebooks
2. **Google Cloud Run** - Containerized, auto-scaling
3. **AWS Lambda** - Serverless, event-driven
4. **Local Development** - Docker or virtual environment

### Batch Processing
```python
async def process_batch(documents: List[str]):
    tasks = [run_compliance_check(doc) for doc in documents]
    results = await asyncio.gather(*tasks)
    return results
```

---

## 🎯 Future Enhancements

1. **Caching Layer** - Cache policy extractions for reuse
2. **Web UI** - Dashboard for compliance teams
3. **Integrations** - Connect to Jira, GitHub, Slack
4. **Custom Models** - Fine-tune on domain-specific data
5. **Batch Processing** - Handle multiple documents in parallel
6. **Report History** - Track compliance changes over time
7. **Advanced Metrics** - Trend analysis and dashboards
8. **Custom Rules** - Allow team-specific compliance rules

---

## 📞 Support & Resources

- **GitHub:** [praxc/ai-enterprise-compliance-agent](https://github.com/praxc/ai-enterprise-compliance-agent)
- **Documentation:** See `docs/` folder
- **Issues:** Report on GitHub
- **License:** MIT

---

## 🎓 Learning Resources

- **ADK Documentation:** [Google Agent Development Kit](https://ai.google.dev/adk)
- **Gemini API:** [Google Generative AI](https://ai.google.dev)
- **Project Course:** Enterprise Agents Intensive Course (Google)

---

**End of Repository Structure Documentation**

