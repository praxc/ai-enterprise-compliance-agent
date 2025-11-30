"""Evaluation script for testing the compliance copilot on labeled data."""

import json
import asyncio
import time
from pathlib import Path
from typing import Dict, Any

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
from src.tools.response_parser import parse_compliance_response
from src.utils.config import get_retry_config, load_api_key


async def run_evaluation(
    policy_path: str,
    test_docs_dir: str,
    gold_labels_path: str
) -> Dict[str, Any]:
    """
    Run evaluation on test dataset.
    
    Args:
        policy_path: Path to policy document
        test_docs_dir: Directory containing test documents
        gold_labels_path: Path to gold labels JSON
        
    Returns:
        Dictionary with evaluation results
    """
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
        app_name="ComplianceEval",
        session_service=session_service
    )
    
    # Load policy
    with open(policy_path, 'r') as f:
        policy_text = f.read()
    
    # Load gold labels
    with open(gold_labels_path, 'r') as f:
        gold_labels = json.load(f)
    
    # Load test documents
    test_docs_path = Path(test_docs_dir)
    test_documents = {}
    for doc_file in test_docs_path.glob("*.txt"):
        with open(doc_file, 'r') as f:
            test_documents[doc_file.name] = f.read()
    
    # Run evaluation
    results = {
        "true_positives": 0,
        "false_positives": 0,
        "false_negatives": 0,
        "true_negatives": 0,
        "processing_times": [],
        "per_document": {}
    }
    
    for doc_name, doc_text in test_documents.items():
        print(f"Evaluating: {doc_name}")
        
        expected = gold_labels.get(doc_name, {})
        expected_count = expected.get("total_violations", 0)
        
        # Run compliance check
        start_time = time.time()
        
        query = f"""
Scan this document for violations:

POLICY:
{policy_text}

DOCUMENT:
{doc_text}

Provide summary with severity breakdown.
        """
        
        query_content = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
        
        response_text = ""
        async for event in runner.run_async(
            user_id="eval",
            session_id=f"eval_{doc_name}",
            new_message=query_content
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        response_text += part.text
        
        elapsed = time.time() - start_time
        results["processing_times"].append(elapsed)
        
        # Parse results
        parsed = parse_compliance_response(response_text)
        actual_count = parsed["total_violations"]
        
        # Calculate metrics
        if expected_count > 0:
            tp = min(actual_count, expected_count)
            fp = max(0, actual_count - expected_count)
            fn = max(0, expected_count - actual_count)
            
            results["true_positives"] += tp
            results["false_positives"] += fp
            results["false_negatives"] += fn
        else:
            if actual_count == 0:
                results["true_negatives"] += 1
            else:
                results["false_positives"] += actual_count
        
        results["per_document"][doc_name] = {
            "expected": expected_count,
            "actual": actual_count,
            "time": elapsed
        }
    
    # Calculate final metrics
    tp = results["true_positives"]
    fp = results["false_positives"]
    fn = results["false_negatives"]
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    results["metrics"] = {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "avg_time": sum(results["processing_times"]) / len(results["processing_times"])
    }
    
    return results


def main():
    """Run evaluation from command line."""
    results = asyncio.run(run_evaluation(
        policy_path="demo_data/sample_policy.txt",
        test_docs_dir="demo_data/test_documents",
        gold_labels_path="demo_data/gold_labels.json"
    ))
    
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    print(f"\nPrecision: {results['metrics']['precision']:.2%}")
    print(f"Recall: {results['metrics']['recall']:.2%}")
    print(f"F1 Score: {results['metrics']['f1_score']:.3f}")
    print(f"Avg Time: {results['metrics']['avg_time']/60:.2f} min/doc")
    print("\nPer-Document Results:")
    for doc, res in results['per_document'].items():
        print(f"  {doc}: Expected {res['expected']}, Found {res['actual']}")


if __name__ == "__main__":
    main()