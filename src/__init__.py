"""
AI Enterprise Compliance Copilot

Multi-agent system for automated compliance checking and violation remediation.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from src.agents.orchestrator import create_orchestrator_agent
from src.agents.policy_extractor import create_policy_extractor_agent
from src.agents.document_scanner import create_document_scanner_agent
from src.agents.violation_analyzer import create_violation_analyzer_agent
from src.agents.rewrite_agent import create_rewrite_agent

__all__ = [
    "create_orchestrator_agent",
    "create_policy_extractor_agent",
    "create_document_scanner_agent",
    "create_violation_analyzer_agent",
    "create_rewrite_agent",
]