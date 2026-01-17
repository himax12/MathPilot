"""
Prompt Loader Utility
Loads prompt templates from external markdown files.
"""

import os
from typing import Optional

# Directory where prompts are stored
PROMPTS_DIR = os.path.dirname(__file__)


def load_prompt(name: str) -> str:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        name: Name of the prompt file (without .md extension)
        
    Returns:
        The prompt template string
        
    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    filepath = os.path.join(PROMPTS_DIR, f"{name}.md")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def format_prompt(name: str, **kwargs) -> str:
    """
    Load a prompt template and format it with the given variables.
    
    Args:
        name: Name of the prompt file
        **kwargs: Variables to substitute in the template
        
    Returns:
        The formatted prompt string
    """
    template = load_prompt(name)
    return template.format(**kwargs)


# Cache loaded prompts for performance
_prompt_cache: dict = {}


def get_prompt(name: str, use_cache: bool = True) -> str:
    """
    Get a prompt with optional caching.
    
    Args:
        name: Name of the prompt file
        use_cache: Whether to use cached version
        
    Returns:
        The prompt template string
    """
    if use_cache and name in _prompt_cache:
        return _prompt_cache[name]
    
    prompt = load_prompt(name)
    
    if use_cache:
        _prompt_cache[name] = prompt
    
    return prompt
