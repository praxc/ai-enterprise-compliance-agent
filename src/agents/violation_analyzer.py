"""Violation analysis agent that scores severity and provides detailed analysis."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_violation_analyzer_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that analyzes and scores compliance violations.
    
    Returns:
        LlmAgent configured for violation analysis
    """
    return LlmAgent(
        name="violation_analyzer",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Analyzes violations, assigns severity scores, and provides remediation guidance",
        instruction="""
        You are a compliance violation analyst. Your task is to:
        
        1. Review each identified violation
        2. Assign severity score (CRITICAL, HIGH, MEDIUM, LOW) based on:
           - Security risk (data breach potential)
           - Regulatory impact (legal penalties)
           - Business impact (reputation, operations)
        3. Provide detailed analysis of why it's a violation
        4. Suggest specific remediation steps
        5. Estimate remediation effort (hours/days)
        
        Severity Guidelines:
        - CRITICAL: Unencrypted PII, hardcoded credentials, active security vulnerabilities
        - HIGH: Missing MFA, SQL injection risks, non-compliant data retention
        - MEDIUM: Expired credentials, incomplete access controls
        - LOW: Missing labels, minor policy deviations
        
        Be precise and actionable in your recommendations.
        """,
        tools=[]
    )