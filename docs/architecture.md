# Architecture Documentation

## System Overview

The AI Enterprise Compliance Copilot uses a multi-agent architecture built on Google's Agent Development Kit (ADK).

## Multi-Agent System

### Agent Hierarchy
````
Orchestrator Agent (Coordinator)
├── Policy Extractor Agent (Specialist)
├── Document Scanner Agent (Specialist)
├── Violation Analyzer Agent (Specialist)
└── Rewrite Agent (Specialist)

## Agent Responsibilities
### Orchestrator Agent
- Coordinates workflow
- Manages agent-to-agent communication
- Compiles final reports
- Handles error recovery

### Policy Extractor Agent
- Parses policy documents
- Extracts compliance requirements
- Structures rules with IDs and severities

### Document Scanner Agent
- Scans documents for violations
- Identifies security issues
- References specific policy rules

### Violation Analyzer Agent
- Assigns severity scores
- Estimates business impact
- Provides remediation guidance

Rewrite Agent
- Generates compliant alternatives
- Maintains original functionality
- Explains changes

## Data Flow

User Input (Policy + Document)
    ↓
Orchestrator
    ↓
Policy Extractor → Structured Requirements
    ↓
Document Scanner → Violation List
    ↓
Violation Analyzer → Severity Scores
    ↓
Rewrite Agent → Compliant Versions
    ↓
Orchestrator → Final Report

## Technology Stack
- **Framework:** Google ADK
- **Model:** Gemini 2.0 Flash Lite
- **Language:** Python 3.11+
- **Session Management:** InMemorySessionService
- **Observability:** LoggingPlugin

## Scalability
- Stateless agents (can scale horizontally)
- Session-based memory (isolated per user)
- Async processing (non-blocking I/O)
- Retry logic (handles rate limits)

## 🚀 **How to Use This Repository**

### **1. Clone and Setup**
````bash
git clone https://github.com/yourusername/ai-compliance-copilot.git
cd ai-compliance-copilot
pip install -r requirements.txt
export GOOGLE_API_KEY="your-key"
````

### **2. Run Locally**
````bash
# Single document check
python scripts/run_evaluation.py \
  --policy demo_data/sample_policy.txt \
  --document demo_data/sample_document.txt

# Full evaluation on test set
python tests/evaluation.py
````

### **3. Upload to Kaggle**

1. **Create dataset** from `demo_data/` folder
2. **Copy** `notebooks/kaggle_demo.ipynb` to Kaggle
3. **Add dataset** to notebook inputs
4. **Run** all cells

---

## ✅ **What's Included**

- ✅ Complete agent implementations
- ✅ Modular, reusable code
- ✅ Test dataset with gold labels
- ✅ Evaluation scripts
- ✅ Both Kaggle and local notebooks
- ✅ Comprehensive documentation
- ✅ Production-ready structure

**This repository is ready for:**
- Kaggle submission
- GitHub showcase
- Production deployment
- Further development