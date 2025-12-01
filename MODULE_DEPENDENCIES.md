# Module Dependency Map

## Import Relationships

```
┌────────────────────────────────────────────────────────────────┐
│ ENTRY POINTS                                                    │
├────────────────────────────────────────────────────────────────┤
│ • scripts/run_evaluation.py                                     │
│ • notebooks/ai-enterprise-compliance-agent.ipynb               │
│ • tests/evaluation.py                                           │
│ • tests/test_agents.py                                         │
│ • tests/test_tools.py                                          │
└────────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ src/__init__ │    │ src.utils    │    │ src.agents   │
│              │    │              │    │              │
│ Exports:     │    │ config.py    │    │ __init__.py  │
│ • orchestr.. │    │ • load_api.. │    │              │
│ • policy..   │    │ • get_retry  │    │ Exports:     │
│ • document.. │    │              │    │ • orchestr.. │
│ • violation. │    │ ↓ imported by│    │ • policy..   │
│ • rewrite    │    │   all agents │    │ • document.. │
│              │    │              │    │ • violation. │
└──────────────┘    └──────────────┘    │ • rewrite    │
        │                                │              │
        │                                └──────────────┘
        │                                      ↓
        │           ┌─────────────────────────────────────────┐
        │           │ SPECIALIZED AGENTS (each imports):      │
        │           │                                         │
        │           │ • from google.adk.agents import         │
        │           │ • from google.adk.models.google_llm     │
        │           │ • from google.adk.tools import          │
        │           │ • from google.genai import types        │
        │           │                                         │
        │           │ orchestrator.py                         │
        │           │ ├─ Wraps all 4 specialist agents       │
        │           │ └─ Delegates to them via AgentTool      │
        │           │                                         │
        │           │ policy_extractor.py                     │
        │           │ ├─ Pure text analysis                   │
        │           │ └─ No dependencies on other agents      │
        │           │                                         │
        │           │ document_scanner.py                     │
        │           │ ├─ Pure text analysis                   │
        │           │ └─ Uses policy_extractor output         │
        │           │                                         │
        │           │ violation_analyzer.py                   │
        │           │ ├─ Pure text analysis                   │
        │           │ └─ Uses document_scanner output         │
        │           │                                         │
        │           │ rewrite_agent.py                        │
        │           │ ├─ Pure text generation                 │
        │           │ └─ Uses violation_analyzer output       │
        │           │                                         │
        └─────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ src/tools    │    │ src/exporter │    │ src/utils    │
│              │    │              │    │              │
│ __init__.py  │    │ __init__.py   │    │ config.py    │
│              │    │              │    │              │
│ pdf_ingesti..│    │ exporter.py   │    │ • load_api.. │
│ • extract_.. │    │ • export_..   │    │ • get_retry  │
│ • parse_pol. │    │ • export_to   │    │              │
│              │    │               │    │ Used by:     │
│ response_p.. │    │ html_templa.. │    │ • All agents │
│ • parse_com. │    │ • HTML_TEMP.. │    │ • All scripts│
│ • extract_v. │    │               │    │              │
│              │    │ pdf_generato. │    └──────────────┘
│ Used by:     │    │ • export_to.. │
│ • Notebooks  │    │               │
│ • Scripts    │    │ Used by:      │
│              │    │ • export_..   │
│              │    │ • Notebooks   │
│              │    │              │
└──────────────┘    └──────────────┘
```

## Dependency Flow (Data Perspective)

```
INPUT DOCUMENTS
    │
    ├──→ src/tools/pdf_ingestion.py
    │    extract_text_from_pdf()
    │    └──→ PyPDF2.PdfReader
    │
    └──→ Raw Text
         │
         ├──→ Policy Text → orchestrator.py
         │                  └──→ policy_extractor.py
         │                       └──→ Policy Requirements (JSON)
         │
         ├──→ Document Text + Policy Requirements
         │    └──→ document_scanner.py
         │         └──→ Violations List (JSON)
         │
         ├──→ Each Violation + Policy
         │    └──→ violation_analyzer.py
         │         └──→ Severity Score + Remediation (JSON)
         │
         ├──→ CRITICAL/HIGH Violations
         │    └──→ rewrite_agent.py
         │         └──→ Compliant Rewrites (JSON)
         │
         └──→ All Aggregated Results
              └──→ orchestrator.py (Final Report)
                   ├──→ EXECUTIVE SUMMARY
                   ├──→ CRITICAL VIOLATIONS
                   ├──→ HIGH VIOLATIONS
                   ├──→ MEDIUM VIOLATIONS
                   └──→ LOW VIOLATIONS

OUTPUT REPORT
    │
    └──→ src/tools/response_parser.py
         ├──→ parse_compliance_response()
         └──→ Structured Metrics (JSON)
              │
              └──→ src/exporter/
                  ├──→ exporter.py → export_to_json()
                  ├──→ exporter.py → export_to_csv()
                  ├──→ exporter.py → export_to_html()
                  │                  (uses html_template.py)
                  └──→ exporter.py → export_to_pdf()
                                     (uses pdf_generator.py)
                                     └──→ reportlab

METRICS & EVALUATION
    │
    └──→ tests/evaluation.py
         ├──→ Loads test documents
         ├──→ Compares vs gold_labels.json
         └──→ Calculates: Precision, Recall, F1, Accuracy
```

## Class & Function Hierarchy

```
src/
├── agents/
│   ├── orchestrator.py
│   │   └── create_orchestrator_agent()
│   │       └── LlmAgent(
│   │           name="compliance_orchestrator",
│   │           model=Gemini(...),
│   │           instruction="SEQUENTIAL WORKFLOW...",
│   │           tools=[
│   │               AgentTool(policy_extractor),
│   │               AgentTool(document_scanner),
│   │               AgentTool(violation_analyzer),
│   │               AgentTool(rewrite_agent)
│   │           ]
│   │       )
│   │
│   ├── policy_extractor.py
│   │   └── create_policy_extractor_agent()
│   │       └── LlmAgent(
│   │           name="policy_extractor",
│   │           model=Gemini(...),
│   │           instruction="EXTRACT REQUIREMENTS...",
│   │           tools=[]
│   │       )
│   │
│   ├── document_scanner.py
│   │   └── create_document_scanner_agent()
│   │       └── LlmAgent(
│   │           name="document_scanner",
│   │           model=Gemini(...),
│   │           instruction="SCAN FOR VIOLATIONS...",
│   │           tools=[]
│   │       )
│   │
│   ├── violation_analyzer.py
│   │   └── create_violation_analyzer_agent()
│   │       └── LlmAgent(
│   │           name="violation_analyzer",
│   │           model=Gemini(...),
│   │           instruction="ANALYZE & SCORE...",
│   │           tools=[]
│   │       )
│   │
│   └── rewrite_agent.py
│       └── create_rewrite_agent()
│           └── LlmAgent(
│               name="rewrite_agent",
│               model=Gemini(...),
│               instruction="GENERATE REWRITES...",
│               tools=[]
│           )
│
├── tools/
│   ├── pdf_ingestion.py
│   │   ├── extract_text_from_pdf(pdf_content: bytes)
│   │   │   └── PyPDF2.PdfReader
│   │   │       └── Returns: Dict[status, text, page_count]
│   │   │
│   │   └── parse_policy_structure(policy_text: str)
│   │       └── Returns: Dict[sections, total_sections]
│   │
│   └── response_parser.py
│       ├── parse_compliance_response(response_text: str)
│       │   ├── Regex patterns for severity counts
│       │   ├── JSON parsing with markdown handling
│       │   └── Returns: Dict[violations, total, severity_counts, rewrites]
│       │
│       └── extract_violation_details(response_text: str)
│           └── Returns: List[Dict[severity, description, ...]]
│
├── exporter/
│   ├── exporter.py
│   │   ├── export_to_json(results, output_path)
│   │   ├── export_to_csv(results, output_path)
│   │   ├── export_to_html(results, output_path)
│   │   ├── export_to_pdf(results, output_path)
│   │   └── export_all(results, base_name, output_dir, fmt="all")
│   │
│   ├── html_template.py
│   │   └── HTML_TEMPLATE (string constant)
│   │
│   └── pdf_generator.py
│       └── export_to_pdf(results, output_path)
│           └── reportlab.platypus.SimpleDocTemplate
│
└── utils/
    └── config.py
        ├── load_api_key()
        │   └── Returns: str (from os.environ["GOOGLE_API_KEY"])
        │
        └── get_retry_config(attempts=5, exp_base=7, ...)
            └── Returns: types.HttpRetryOptions
                ├── attempts: 5
                ├── exp_base: 7
                ├── initial_delay: 1
                └── http_status_codes: [429, 500, 503, 504]
```

## Runtime Dependencies (Import Order)

```
Step 1: Load Environment
  └── os.environ["GOOGLE_API_KEY"]

Step 2: Initialize Configuration
  └── src.utils.config
      ├── load_api_key()
      └── get_retry_config()

Step 3: Create Agents
  ├── src.agents.policy_extractor.create_policy_extractor_agent()
  ├── src.agents.document_scanner.create_document_scanner_agent()
  ├── src.agents.violation_analyzer.create_violation_analyzer_agent()
  ├── src.agents.rewrite_agent.create_rewrite_agent()
  └── src.agents.orchestrator.create_orchestrator_agent()
      └── (wraps above 4 agents as tools)

Step 4: Setup Runner
  ├── google.adk.sessions.InMemorySessionService
  └── google.adk.runners.Runner

Step 5: Load Documents
  └── src.tools.pdf_ingestion.extract_text_from_pdf()

Step 6: Run Compliance Check
  ├── orchestrator.run_async()
  └── Returns: compliance report (text)

Step 7: Parse Results
  └── src.tools.response_parser.parse_compliance_response()
      └── Returns: Dict[violations by severity]

Step 8: Export Report
  └── src.exporter.exporter.export_all()
      ├── export_to_json()
      ├── export_to_csv()
      ├── export_to_html() → html_template.py
      └── export_to_pdf() → pdf_generator.py
```

## External Dependencies Map

```
google-adk 0.1.0+
├── google.adk.agents.LlmAgent
├── google.adk.models.google_llm.Gemini
├── google.adk.tools.AgentTool
├── google.adk.runners.Runner
├── google.adk.sessions.InMemorySessionService
└── google.adk.plugins.logging_plugin.LoggingPlugin

google-generativeai 0.8.0+
├── google.genai.types
│   ├── types.HttpRetryOptions
│   ├── types.Content
│   ├── types.Part
│   └── types.GenerateContentConfig
└── google.genai (main module)

PyPDF2 3.0.0+
├── PyPDF2.PdfReader
└── (for PDF text extraction)

reportlab 4.0.0+ (optional, for PDF export)
├── reportlab.lib.pagesizes.A4
├── reportlab.lib.styles.getSampleStyleSheet
└── reportlab.platypus (PDF generation)

Standard Library
├── os (environment variables)
├── io (BytesIO for PDF handling)
├── asyncio (async/await)
├── typing (type hints)
├── datetime (timestamps)
├── re (regex for parsing)
├── json (JSON parsing)
├── csv (CSV writing)
├── pathlib (file paths)
└── argparse (CLI arguments)

Testing & Development
├── pytest 7.4.0+
├── pytest-asyncio 0.21.0+
├── jupyter 1.0.0+
├── ipykernel 6.0.0+
└── python-dotenv 1.0.0+ (optional)
```

---

**Generated:** December 1, 2025  
**Project:** AI Enterprise Compliance Copilot v1.0.0

