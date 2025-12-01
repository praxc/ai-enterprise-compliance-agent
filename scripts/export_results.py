#!/usr/bin/env python3
"""Export compliance results to various formats."""

import json
from pathlib import Path
from argparse import ArgumentParser
from src.exporter.exporter import export_all


def main():
    """Export results from JSON file to multiple formats."""
    parser = ArgumentParser(description="Export compliance results")
    parser.add_argument("--input", required=True, help="Path to input JSON results file")
    parser.add_argument("--format", choices=["json", "csv", "html", "pdf", "all"], 
                       default="all", help="Export format (default: all)")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")
    
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {args.input}")
    
    # Load results
    try:
        with open(input_path, 'r') as f:
            results = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")
    
    # Export
    base_name = input_path.stem
    export_all(results, base_name=base_name, output_dir=args.output_dir, fmt=args.format)
    
    print(f"✅ Export completed to: {args.output_dir}/")


if __name__ == "__main__":
    main()