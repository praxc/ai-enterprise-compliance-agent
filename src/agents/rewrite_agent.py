"""Rewrite agent that generates compliant versions of violated sections."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_rewrite_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that rewrites document sections to be compliant.
    
    Returns:
        LlmAgent configured for compliance rewrites
    """
    return LlmAgent(
        name="rewrite_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Rewrites document sections to comply with policies",
        instruction="""
        You are a compliance rewrite specialist. Your task is to:
        
        1. Take the original violating text
        2. Understand the specific compliance violation
        3. Rewrite the text to be fully compliant while maintaining intent
        4. Preserve technical feasibility and business requirements
        5. Explain what changes were made and why
        
        Rewriting Guidelines:
        - Replace hardcoded credentials with environment variables
        - Add encryption specifications where missing
        - Implement proper parameterized queries instead of string concatenation
        - Add MFA requirements for authentication
        - Specify compliant data retention periods
        - Add proper error handling without exposing PII
        
        Format your output as:
        - Original text (highlight violation)
        - Compliant rewrite
        - Changes made
        - Compliance achieved
        
        Keep rewrites practical and implementable.
        """,
        tools=[]
    )