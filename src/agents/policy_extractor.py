"""Policy extraction agent that extracts compliance rules from policy documents."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_policy_extractor_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that extracts structured compliance requirements from policy documents.
    
    Args:
        retry_config: HTTP retry configuration for API calls
        
    Returns:
        LlmAgent configured for policy extraction
    """
    return LlmAgent(
        name="policy_extractor",
        model=Gemini(model="gemini-2.0-flash-lite", retry_options=retry_config),
        description="Extracts and structures compliance requirements from policy documents",
        instruction="""
        You are a policy extraction specialist. Your task is to:
        
        1. Read the provided policy document text carefully
        2. Extract ALL compliance requirements and rules
        3. Identify severity levels for violations (CRITICAL, HIGH, MEDIUM, LOW)
        4. Structure requirements as clear, actionable rules
        5. Note any specific metrics or thresholds (e.g., "within 72 hours", "AES-256")
        
        Output Format:
        For each requirement, provide:
        - Rule ID (e.g., SEC-1.1, ACCESS-2.3)
        - Category (e.g., Data Security, Access Control, Data Retention)
        - Requirement description (clear and specific)
        - Severity level if violated
        - Key metrics or constraints
        
        Be thorough and precise. Every requirement matters for compliance.
        Extract even minor requirements - they all count.
        """,
        tools=[]  # No tools needed - pure text analysis
    )