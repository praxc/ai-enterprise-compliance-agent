"""Unit tests for tools."""

import pytest
import io
from pathlib import Path

from src.tools.pdf_ingestion import extract_text_from_pdf, parse_policy_structure
from src.tools.response_parser import parse_compliance_response, extract_violation_details


class TestPDFIngestion:
    """Tests for PDF ingestion tools."""
    
    def test_parse_policy_structure_basic(self):
        """Test parsing a simple policy structure."""
        policy_text = """
        SECTION 1: DATA SECURITY
        1.1 All data must be encrypted.
        1.2 Use AES-256 encryption.
        
        SECTION 2: ACCESS CONTROL
        2.1 Require MFA for all access.
        """
        
        result = parse_policy_structure(policy_text)
        
        assert result["status"] == "success"
        assert result["total_sections"] == 2
        assert "SECTION 1: DATA SECURITY" in result["sections"]
        assert "SECTION 2: ACCESS CONTROL" in result["sections"]
    
    def test_parse_policy_structure_empty(self):
        """Test parsing empty policy."""
        result = parse_policy_structure("")
        
        assert result["status"] == "success"
        assert result["total_sections"] == 0


class TestResponseParser:
    """Tests for response parser."""
    
    def test_parse_compliance_response_with_violations(self):
        """Test parsing response with violations."""
        response_text = """
        COMPLIANCE CHECK RESULTS:
        
        🔴 CRITICAL: 2
        - Hardcoded API key
        - Unencrypted PII
        
        🟠 HIGH: 3
        - Missing MFA
        - SQL injection risk
        - PII in logs
        
        🟡 MEDIUM: 1
        - Expired credentials
        
        ✅ COMPLIANT REWRITE:
        Use environment variables for API keys
        
        ✅ COMPLIANT REWRITE:
        Encrypt all PII data
        """
        
        result = parse_compliance_response(response_text)
        
        assert result["total_violations"] == 6  # 2 + 3 + 1
        assert result["severity_counts"]["CRITICAL"] == 2
        assert result["severity_counts"]["HIGH"] == 3
        assert result["severity_counts"]["MEDIUM"] == 1
        assert result["severity_counts"]["LOW"] == 0
        assert result["rewrites_generated"] == 2
    
    def test_parse_compliance_response_clean(self):
        """Test parsing response with no violations."""
        response_text = """
        COMPLIANCE CHECK RESULTS:
        
        No violations found. Document is fully compliant.
        """
        
        result = parse_compliance_response(response_text)
        
        assert result["total_violations"] == 0
        assert result["rewrites_generated"] == 0
    
    def test_parse_compliance_response_various_formats(self):
        """Test parsing various response formats."""
        response_text = """
        Found CRITICAL violations: 1
        HIGH severity issues: 2
        3 MEDIUM problems detected
        """
        
        result = parse_compliance_response(response_text)
        
        assert result["severity_counts"]["CRITICAL"] >= 1
        assert result["severity_counts"]["HIGH"] >= 2
        assert result["severity_counts"]["MEDIUM"] >= 3
    
    def test_extract_violation_details(self):
        """Test extracting detailed violation information."""
        response_text = """
        CRITICAL: Hardcoded password in config.py line 42
        HIGH: Missing MFA for admin panel
        MEDIUM: API keys not rotated in 120 days
        """
        
        violations = extract_violation_details(response_text)
        
        assert len(violations) >= 3
        assert any(v["severity"] == "CRITICAL" for v in violations)
        assert any(v["severity"] == "HIGH" for v in violations)
        assert any(v["severity"] == "MEDIUM" for v in violations)


class TestIntegration:
    """Integration tests for tools."""
    
    def test_end_to_end_parsing(self):
        """Test complete parsing workflow."""
        # Policy
        policy_text = """
        SECTION 1: SECURITY
        1.1 Encrypt all data
        """
        
        policy_result = parse_policy_structure(policy_text)
        assert policy_result["status"] == "success"
        
        # Response
        response_text = """
        🔴 CRITICAL: 1
        Unencrypted customer data found
        
        ✅ COMPLIANT REWRITE:
        Encrypt data using AES-256
        """
        
        response_result = parse_compliance_response(response_text)
        assert response_result["total_violations"] == 1
        assert response_result["rewrites_generated"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])