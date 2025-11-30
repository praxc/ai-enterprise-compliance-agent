"""Response parser for extracting structured data from agent outputs."""

import re
from typing import Dict, List, Any


def parse_compliance_response(response_text: str) -> Dict[str, Any]:
    """
    Parse the agent's response to extract violations dynamically.
    
    Args:
        response_text: Raw text response from compliance agent
        
    Returns:
        Dictionary with violations by severity and other metrics
    """
    violations = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "LOW": []
    }
    
    total_violations = 0
    rewrites_generated = 0
    
    # Extract severity counts using regex patterns
    severity_patterns = {
        "CRITICAL": r"(?:🔴|CRITICAL)[:\s]*(\d+)|(\d+)\s*(?:CRITICAL|critical)",
        "HIGH": r"(?:🟠|HIGH)[:\s]*(\d+)|(\d+)\s*(?:HIGH|high)",
        "MEDIUM": r"(?:🟡|MEDIUM)[:\s]*(\d+)|(\d+)\s*(?:MEDIUM|medium)",
        "LOW": r"(?:🟢|LOW)[:\s](\d+)|(\d+)\s(?:LOW|low)"
        }

    for severity, pattern in severity_patterns.items():
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        if matches:
            # Get the first non-empty match
            count = next((int(m) for group in matches for m in group if m), 0)
            violations[severity] = [{"id": f"{severity}_{i+1}"} for i in range(count)]

    # Count total violations
    total_violations = sum(len(v) for v in violations.values())

    # Count rewrites (look for "COMPLIANT REWRITE" or similar patterns)
    rewrite_patterns = [
        r"✅\s*COMPLIANT\s+REWRITE",
        r"COMPLIANT\s+VERSION",
        r"REWRITE\s*:",
        r"Fixed\s+version"
    ]

    for pattern in rewrite_patterns:
        rewrites_generated += len(re.findall(pattern, response_text, re.IGNORECASE))

    return {
        "violations": violations,
        "total_violations": total_violations,
        "severity_counts": {k: len(v) for k, v in violations.items()},
        "rewrites_generated": rewrites_generated
    }

def extract_violation_details(response_text: str) -> List[Dict[str, Any]]:
    """
    Extract detailed information about each violation.

    Args:
        response_text: Raw text response from compliance agent
        
    Returns:
        List of violation dictionaries with details
    """
    violations = []

    # Pattern to match violation blocks
    # This is a simplified version - production would be more sophisticated
    violation_pattern = r"(CRITICAL|HIGH|MEDIUM|LOW):\s*(.+?)(?=(?:CRITICAL|HIGH|MEDIUM|LOW):|$)"

    matches = re.findall(violation_pattern, response_text, re.DOTALL | re.IGNORECASE)

    for severity, description in matches:
        violations.append({
            "severity": severity.upper(),
            "description": description.strip(),
            "extracted_from": "agent_response"
        })

    return violations
