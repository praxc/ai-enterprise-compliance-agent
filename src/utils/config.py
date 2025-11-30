"""Configuration utilities for the compliance copilot."""

import os
from google.genai import types
from typing import Optional


def load_api_key() -> str:
    """
    Load Google API key from environment.
    
    Returns:
        API key string
        
    Raises:
        ValueError: If API key not found
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment. "
            "Please set it using: export GOOGLE_API_KEY='your-key-here'"
        )
    
    return api_key


def get_retry_config(
    attempts: int = 5,
    exp_base: int = 7,
    initial_delay: int = 1,
    http_status_codes: Optional[list] = None
) -> types.HttpRetryOptions:
    """
    Get retry configuration for API calls.
    
    Args:
        attempts: Maximum number of retry attempts
        exp_base: Exponential backoff base
        initial_delay: Initial delay in seconds
        http_status_codes: List of HTTP status codes to retry on
        
    Returns:
        HttpRetryOptions configuration
    """
    if http_status_codes is None:
        http_status_codes = [429, 500, 503, 504]
    
    return types.HttpRetryOptions(
        attempts=attempts,
        exp_base=exp_base,
        initial_delay=initial_delay,
        http_status_codes=http_status_codes
    )