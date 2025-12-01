"""Unit tests for agent implementations."""

import pytest
import asyncio
from google.genai import types

from src.agents import (
    create_policy_extractor_agent,
    create_document_scanner_agent,
    create_violation_analyzer_agent,
    create_rewrite_agent,
    create_orchestrator_agent,
)
from src.utils.config import get_retry_config


@pytest.fixture
def retry_config():
    """Fixture for retry configuration."""
    return get_retry_config(attempts=3)


@pytest.fixture
def sample_policy():
    """Fixture for sample policy text."""
    return """
    SECTION 1: DATA SECURITY
    1.1 All data must be encrypted at rest using AES-256.
    1.2 Customer PII must not be stored in logs.
    """


@pytest.fixture
def sample_document():
    """Fixture for sample document with violations."""
    return """
    FEATURE: User Dashboard
    
    Implementation:
    - Customer data stored in plaintext files
    - API Key: sk_live_abc123 (hardcoded)
    - Logging: Log all user emails for debugging
    """


class TestPolicyExtractorAgent:
    """Tests for Policy Extractor Agent."""
    
    def test_agent_creation(self, retry_config):
        """Test that policy extractor agent can be created."""
        agent = create_policy_extractor_agent(retry_config)
        
        assert agent is not None
        assert agent.name == "policy_extractor"
        assert "policy extraction" in agent.description.lower()
    
    def test_agent_has_no_tools(self, retry_config):
        """Test that policy extractor has no tools (pure text analysis)."""
        agent = create_policy_extractor_agent(retry_config)
        
        assert len(agent.tools) == 0


class TestDocumentScannerAgent:
    """Tests for Document Scanner Agent."""
    
    def test_agent_creation(self, retry_config):
        """Test that document scanner agent can be created."""
        agent = create_document_scanner_agent(retry_config)
        
        assert agent is not None
        assert agent.name == "document_scanner"
        assert "scan" in agent.description.lower()
    
    def test_agent_has_no_tools(self, retry_config):
        """Test that document scanner has no tools."""
        agent = create_document_scanner_agent(retry_config)
        
        assert len(agent.tools) == 0


class TestViolationAnalyzerAgent:
    """Tests for Violation Analyzer Agent."""
    
    def test_agent_creation(self, retry_config):
        """Test that violation analyzer agent can be created."""
        agent = create_violation_analyzer_agent(retry_config)
        
        assert agent is not None
        assert agent.name == "violation_analyzer"
        assert "violation" in agent.description.lower()
    
    def test_instruction_contains_severity_levels(self, retry_config):
        """Test that instruction includes severity guidelines."""
        agent = create_violation_analyzer_agent(retry_config)
        
        instruction = agent.instruction.lower()
        assert "critical" in instruction
        assert "high" in instruction
        assert "medium" in instruction
        assert "low" in instruction


class TestRewriteAgent:
    """Tests for Rewrite Agent."""
    
    def test_agent_creation(self, retry_config):
        """Test that rewrite agent can be created."""
        agent = create_rewrite_agent(retry_config)
        
        assert agent is not None
        assert agent.name == "rewrite_agent"
        assert "rewrite" in agent.description.lower()
    
    def test_instruction_contains_rewrite_guidelines(self, retry_config):
        """Test that instruction includes rewrite guidelines."""
        agent = create_rewrite_agent(retry_config)
        
        instruction = agent.instruction.lower()
        assert "compliant" in instruction
        assert "rewrite" in instruction


class TestOrchestratorAgent:
    """Tests for Orchestrator Agent."""
    
    def test_agent_creation(self, retry_config):
        """Test that orchestrator agent can be created."""
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
        
        assert orchestrator is not None
        assert orchestrator.name == "compliance_orchestrator"
    
    def test_orchestrator_has_four_tools(self, retry_config):
        """Test that orchestrator has all 4 specialist agents as tools."""
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
        
        assert len(orchestrator.tools) == 4
    
    def test_instruction_contains_workflow_steps(self, retry_config):
        """Test that orchestrator instruction includes workflow steps."""
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
        
        instruction = orchestrator.instruction.lower()
        assert "step 1" in instruction
        assert "step 2" in instruction
        assert "step 3" in instruction
        assert "step 4" in instruction
        assert "step 5" in instruction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])