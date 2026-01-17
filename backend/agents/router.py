"""
Router Agent - Classifies math problems to determine strategy and knowledge retrieval.
"""

from google import genai
from typing import Dict, List, Optional, Any
import json
import re
import sys
import os

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from agents.base import BaseAgent
from schemas import RouteDecision
from config import config

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
                subtopic=data.get("subtopic", "general_math"),
                strategy=data.get("strategy", "direct_computation"),
                rag_filters=data.get("rag_filters", []),
                confidence=data.get("confidence", 0.5)
            )
            
        except Exception as e:
            self._log(f"Routing failed: {e}")
            # Fallback
            return RouteDecision(
                domain="general", 
                subtopic="unknown", 
                strategy="direct_computation", 
                confidence=0.0
            )
            
    def _build_prompt(self, problem: str) -> str:
        return f"""
Analyze this math problem and classify it for a solver system.

PROBLEM: "{problem}"

Your goal is to output a JSON object with:
1. "domain": High-level subject (Algebra, Calculus, Probability, Geometry, Statistics, Linear Algebra)
2. "subtopic": Specific topic (e.g., "quadratic_equations", "bayes_theorem", "optimization")
3. "strategy": The best algorithmic approach (e.g., "quadratic_formula", "substitution_method", "integration_by_parts")
4. "rag_filters": List of knowledge base keys to search (e.g., ["algebra/quadratics", "calculus/derivatives"])
5. "confidence": Float 0.0-1.0 representing your certainty.

Valid Knowledge Base Keys:
- algebra/basics, algebra/quadratics, algebra/logarithms
- calculus/derivatives, calculus/integration, calculus/limits
- probability/basics, probability/distributions, probability/bayes
- geometry/triangles, geometry/circles
- statistics/descriptive, statistics/inference

OUTPUT format must be PURE JSON (no markdown fences):
{{
    "domain": "...",
    "subtopic": "...",
    "strategy": "...",
    "rag_filters": ["..."],
    "confidence": 0.95
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
