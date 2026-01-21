"""
Router Agent - Classifies math problems to determine strategy and knowledge retrieval.
"""

from google import genai
from typing import Dict, List, Optional, Any
import json
import re

from backend.agents.base import BaseAgent
from backend.schemas import RouteDecision
from backend.config import config

class RouterAgent(BaseAgent):
    """
    The Traffic Controller of the system.
    
    Responsibilities:
    1. Identify broad DOMAIN (Algebra, Calculus, etc.)
    2. Pinpoint specific SUBTOPIC (Quadratic Equations, Integration by Parts)
    3. Recommend a STRATEGY (Factorization, Substitution)
    4. Define RAG FILTERS (which knowledge base files to search)
    """
    
    def route(self, problem_text: str) -> RouteDecision:
        """
        Analyze the problem and determine the routing strategy.
        
        Args:
            problem_text: The natural language math problem.
            
        Returns:
            RouteDecision object with classification details.
        """
        if not problem_text:
            return RouteDecision(
                domain="unknown", 
                subtopic="unknown", 
                strategy="general_solving", 
                confidence=0.0
            )

        prompt = self._build_prompt(problem_text)
        
        try:
            # Use JSON mode if available or standard generation
            response_text = self._call_llm(prompt)
            
            # Clean and parse JSON
            cleaned_json = self._clean_json(response_text)
            data = json.loads(cleaned_json)
            
            return RouteDecision(
                domain=data.get("domain", "general"),
                strategy=data.get("strategy", "direct_computation")
            )
            
        except Exception as e:
            self._log(f"Routing failed: {e}")
            # Fallback
            return RouteDecision(
                domain="general", 
                strategy="direct_computation"
            )
            
    def _build_prompt(self, problem: str) -> str:
        return f"""
Analyze this math problem and classify it for a solver system.

PROBLEM: "{problem}"

Your goal is to output a JSON object with:
1. "domain": High-level subject (Algebra, Calculus, Probability, Geometry, Statistics, Linear Algebra)
2. "strategy": The best algorithmic approach (e.g., "quadratic_formula", "substitution_method", "integration_by_parts")

OUTPUT format must be PURE JSON (no markdown fences):
{{
    "domain": "...",
    "strategy": "..."
}}
"""

    def _clean_json(self, text: str) -> str:
        """Helper to extract JSON from potentially messy LLM output."""
        text = text.strip()
        # Remove markdown fences if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
