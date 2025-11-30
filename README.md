# AI Enterprise Compliance Copilot 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

**Multi-Agent AI System for Enterprise Document Compliance**

A modular AI tool that automatically detects compliance gaps in enterprise documents, scores severity, and generates suggested rewrites — reducing manual review effort and improving consistency.

---

## 🔹 Overview
Enterprises spend thousands of hours manually reviewing SOPs, proposals, contracts, and reports to ensure compliance with internal policies and standards (ISO, SOC2, GDPR, etc.).  

The **AI Enterprise Compliance Copilot** automates this workflow using specialized AI agents that:

- Extract structured rules from policy documents  
- Scan new documents for potential violations  
- Score severity and explain evidence  
- Generate compliant rewrites  
- Learn from accepted corrections to improve future suggestions  

---

## 🔹 Architecture
![Architecture Diagram](docs/architecture_diagram.png)

**Core Agents:**
- **Policy Extraction Agent** – Converts policy documents (PDF, Word) into structured rules.  
- **Document Scanner Agent** – Parses target documents and identifies potential violations.  
- **Violation Analysis Agent** – Computes severity scores, groups issues, and explains evidence.  
- **Rewrite & Remediation Agent** – Suggests compliant text and corrective actions.  
- **Memory Bank** – Stores organization-specific rules and past corrections.  
- **Orchestrator** – Coordinates agent workflows, retries, and produces an audit trail.

---

## 🔹 Tech Stack
- **ADK-Python** – Multi-agent orchestration (Loop, Sequential, Parallel patterns)  
- **LLM:** Gemini API – semantic parsing, policy extraction, and rewrite generation  
- **Tools & Integrations:** PDF parsers, OpenAPI connectors, code execution for reports  
- **Memory & Vector Storage:** FAISS-style vector store for embeddings and long-term memory  
- **Notebook Demo:** Jupyter notebook for end-to-end reproducibility

---

## 🔹 Installation
1. Clone the repository:
git clone https://github.com/<username>/ai-enterprise-compliance-copilot.git
cd ai-enterprise-compliance-copilot

2. Install dependencies:
pip install -r requirements.txt

3. Set your Gemini API key (replace YOUR_KEY_HERE):
export GEMINI_API_KEY="YOUR_KEY_HERE"
