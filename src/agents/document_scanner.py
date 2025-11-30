"""Document scanner agent that analyzes documents for potential compliance issues."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types


def create_document_scanner_agent(retry_config: types.HttpRetryOptions):
    """
    Creates an agent that scans documents for compliance violations.
    
    Args:
        retry_config: HTTP retry configuration for API calls
        
    Returns:
        LlmAgent configured for document scanning
    """
    return LlmAgent(
        name="document_scanner",
        model=Gemini(model="gemini-2.0-flash-lite", retry_options=retry_config),
        description="Scans documents to identify potential compliance violations",
        instruction="""
        You are a document compliance scanner. Your task is to:
        
        1. Read the document text carefully
        2. Compare against the provided compliance requirements
        3. Identify any practices, implementations, or statements that violate policy
        4. Look for security issues: 
           - Hardcoded credentials, API keys, passwords
           - Unencrypted sensitive data (PII, financial info)
           - SQL injection vulnerabilities (string concatenation in queries)
           - Missing encryption specifications
        5. Check access control: 
           - Missing MFA requirements
           - Weak authentication methods
           - Overly permissive access
        6. Verify data handling: 
           - Non-compliant retention policies
           - Improper PII handling
           - Missing encryption requirements
        
        For each potential violation found, provide:
        - Specific text/code snippet that violates policy (exact quote)
        - Section or line reference where found
        - Brief explanation of WHY it's a violation
        - Which policy rule it violates (reference the rule ID)
        
        Be thorough but precise. Only flag CLEAR violations, not hypotheticals.
        If something is ambiguous, note it separately as "needs clarification".
        """,
        tools=[]
    )