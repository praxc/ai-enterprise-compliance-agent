"""Violation analysis agent that scores severity and provides detailed analysis."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_violation_analyzer_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that analyzes and scores compliance violations.
    
    Args:
        retry_config: HTTP retry configuration for API calls
        
    Returns:
        LlmAgent configured for violation analysis
    """
    return LlmAgent(
        name="violation_analyzer",
        model=Gemini(model="gemini-2.0-flash-lite", retry_options=retry_config),
        description="Analyzes violations, assigns severity scores, and provides remediation guidance",
        instruction="""
        You are a compliance violation analyst. Your task is to:
        
        1. Review each identified violation carefully
        2. Assign severity score (CRITICAL, HIGH, MEDIUM, LOW) based on:
           - Security risk: potential for data breach, unauthorized access
           - Regulatory impact: legal penalties, compliance fines
           - Business impact: reputation damage, operational disruption
        3. Provide detailed analysis of WHY it's a violation
        4. Suggest specific, actionable remediation steps
        5. Estimate remediation effort (hours or days)
        
        Severity Guidelines:
        
        🔴 CRITICAL: 
        - Unencrypted customer PII or financial data
        - Hardcoded credentials, API keys, passwords in code
        - Active security vulnerabilities (SQL injection, XSS)
        - Data breach potential
        
        🟠 HIGH: 
        - Missing MFA for sensitive systems
        - SQL injection risks from poor coding practices
        - Non-compliant data retention (violates regulations)
        - Missing encryption for sensitive data in transit
        
        🟡 MEDIUM: 
        - Expired API keys or credentials
        - Incomplete access controls or reviews
        - Missing audit logging
        
        🟢 LOW: 
        - Missing data classification labels
        - Minor documentation issues
        - Style/formatting violations
        
        For each violation provide:
        - Severity score with justification
        - Detailed explanation of risk
        - Step-by-step remediation plan
        - Estimated fix time
        - Priority ranking
        
        Be precise and actionable in your recommendations.
        """,
        tools=[]
    )