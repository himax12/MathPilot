"""
Text processing utilities for Math Mentor.
Centralized functions for cleaning and formatting LLM responses.
"""

import re
from typing import Optional


def strip_code_from_reasoning(reasoning: Optional[str]) -> str:
    """
    Remove code blocks and internal markers from LLM reasoning.
    
    Args:
        reasoning: Raw reasoning text from LLM (may be None)
        
    Returns:
        Cleaned reasoning text, or empty string if None
    """
    if not isinstance(reasoning, str) or reasoning is None:
        return ''
    
    # Remove internal code sections
    reasoning = re.sub(r'\*\*Internal Code\*\*.*', '', reasoning, 
                      flags=re.DOTALL | re.IGNORECASE)
    
    # Remove markdown code blocks
    reasoning = re.sub(r'```[^`]*```', '', reasoning, flags=re.DOTALL)
    
    # Clean up extra whitespace
    return reasoning.strip()


def extract_json_from_markdown(text: str) -> str:
    """
    Remove markdown code fences from JSON responses.
    
    Args:
        text: Text potentially containing ```json ... ``` markers
        
    Returns:
        Cleaned text suitable for JSON parsing
    """
    text = text.strip()
    
    # Remove markdown fences
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    return text.strip()


def extract_code_from_response(response_text: str) -> Optional[str]:
    """
    Extract Python code from LLM response with various formats.
    
    Handles:
    - ```python ... ```
    - ```\n ... \n```
    - Plain code (no markers)
    
    Args:
        response_text: Raw LLM response
        
    Returns:
        Extracted code or the original text if no markers found
    """
    # Try to find code block with python marker
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, response_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # Try generic code block
    pattern = r"```\s*(.*?)\s*```"
    match = re.search(pattern, response_text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # Return as-is (might be plain code)
    return response_text.strip()
