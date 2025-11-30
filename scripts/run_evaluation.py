#!/usr/bin/env python3
"""Script to run compliance check on a single document."""

import argparse
import asyncio
import os
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agents import (
    create_orchestrator_agent,
    create_policy_extractor_agent,
    create_document_scanner_agent,
    create_violation_analyzer_agent,
    create_rewrite_agent,
)
from src.utils.config import get_retry_config, load_api_key


async def run_single_check(policy_path: str, document_path: str):
    """Run compliance check on a single document."""
    # Load API key
    load_api_key()
    
    # Create agents
    retry_config = get_retry_config()
    
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
    
    # Setup runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator,
        app_name="ComplianceCheck",
        session_service=session_service
    )
    
    # Load files
    with open(policy_path, 'r') as f:
        policy_text = f.read()
    
    with open(document_path, 'r') as f:
        document_text = f.read()
    
    # Run check
    query = f"""
Perform complete compliance check:

POLICY:
{policy_text}

DOCUMENT:
{document_text}

Provide detailed analysis with violations and rewrites.
    """
    
    query_content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    print("Running compliance check...\n")
    
    async for event in runner.run_async(
        user_id="cli_user",
        session_id="cli_session",
        new_message=query_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text'):
                    print(part.text)


def main():
    parser = argparse.ArgumentParser(description="Run compliance check")
    parser.add_argument("--policy", required=True, help="Path to policy document")
    parser.add_argument("--document", required=True, help="Path to document to check")
    
    args = parser.parse_args()
    
    asyncio.run(run_single_check(args.policy, args.document))


if __name__ == "__main__":
    main()