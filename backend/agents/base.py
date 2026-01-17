"""
Base Agent - Common functionality for all agents.
DRY principle: shared initialization, logging, error handling.
"""

from google import genai
from typing import Dict, Any, Optional
import logging

import sys
import os

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from config import config


class BaseAgent:
    """
    Base class for all Math Mentor agents.
    
    Provides:
    - Gemini client initialization
    - Consistent logging
    - Error handling wrapper
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize agent with Gemini client.
        
        Args:
            model_name: Gemini model (uses config default if not specified)
        """
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        # Store API key and cache client instance
        self._api_key = config.GEMINI_API_KEY
        self._client_instance = None
        self.model_name = model_name or config.GEMINI_MODEL
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @property
    def client(self):
        """Lazy-init and cache client."""
        if self._client_instance is None:
            self._client_instance = genai.Client(api_key=self._api_key)
        return self._client_instance
    
    def _call_llm(self, prompt: str, **kwargs) -> str:
        """
        Call Gemini with error handling.
        
        Args:
            prompt: The prompt to send
            **kwargs: Additional arguments for generate_content
            
        Returns:
            Response text
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                **kwargs
            )
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            raise
    
    def _log(self, message: str, level: str = "info"):
        """Consistent logging."""
        getattr(self.logger, level)(message)
