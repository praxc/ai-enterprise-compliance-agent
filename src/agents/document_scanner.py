"""Document scanner agent that analyzes documents for potential compliance issues."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_document_scanner_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that scans documents for compliance violations.
    
    Returns:
        LlmAgent configured for document scanning
    """
    return LlmAgent(
        name="document_scanner",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Scans documents to identify potential compliance violations",
        instruction="""
        You are a document compliance scanner. Your task is to:
        
        1. Read the document text carefully
        2. Identify any practices, implementations, or statements that may violate compliance
        3. Look for security issues: hardcoded credentials, unencrypted data, SQL injection risks
        4. Check access control: missing MFA, weak authentication
        5. Verify data handling: retention policies, PII handling, encryption
        
        For each potential violation found, provide:
        - Specific text/code snippet that violates policy
        - Line number or section reference
        - Brief explanation of the issue
        - Applicable policy reference
        
        Be thorough but don't report false positives. Only flag clear violations.
        """,
        tools=[]
    )