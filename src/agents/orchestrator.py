"""Orchestrator agent that coordinates the compliance workflow."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.genai import types


def create_orchestrator_agent(
    policy_extractor,
    document_scanner,
    violation_analyzer,
    rewrite_agent,
    retry_config: types.HttpRetryOptions
):
    """
    Creates the main orchestrator agent that coordinates compliance checking.
    
    Args:
        policy_extractor: Policy extraction agent
        document_scanner: Document scanning agent
        violation_analyzer: Violation analysis agent
        rewrite_agent: Rewrite agent
        retry_config: Retry configuration
        
    Returns:
        LlmAgent configured as orchestrator
    """
    return LlmAgent(
        name="compliance_orchestrator",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Orchestrates the complete compliance checking workflow",
        instruction="""
        You are the Compliance Copilot orchestrator. You coordinate a team of specialist agents
        to perform comprehensive compliance checking. Your workflow is:
        
        STEP 1: Policy Extraction
        - Delegate to policy_extractor agent
        - Input: Policy document text
        - Output: Structured list of compliance requirements
        
        STEP 2: Document Scanning
        - Delegate to document_scanner agent
        - Input: Document to check + extracted policies
        - Output: List of potential violations
        
        STEP 3: Violation Analysis (for each violation)
        - Delegate to violation_analyzer agent
        - Input: Violation details + policy reference
        - Output: Severity score + remediation guidance
        
        STEP 4: Generate Rewrites (for HIGH/CRITICAL violations)
        - Delegate to rewrite_agent
        - Input: Violating text + policy requirement
        - Output: Compliant rewrite
        
        STEP 5: Compile Report
        - Aggregate all results
        - Create structured compliance report
        - Include metrics: total violations, severity breakdown, estimated fix time
        
        Always follow this workflow sequentially. Be thorough and professional.
        """,
        tools=[
            AgentTool(agent=policy_extractor),
            AgentTool(agent=document_scanner),
            AgentTool(agent=violation_analyzer),
            AgentTool(agent=rewrite_agent)
        ]
    )