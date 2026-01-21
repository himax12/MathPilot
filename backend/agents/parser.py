"""
Parser Agent - Understands math problems and structures them for solving.
Bridges the gap between OCR (raw text) and Solver (code generation).
"""

from google import genai
from typing import Dict

from backend.config import config
from backend.agents.base import BaseAgent


class ParserAgent(BaseAgent):
    """
    Understands math problems and extracts actionable information.
    
    Input: OCR output (full problem text)
    Output: Structured problem representation
    
    This solves the "context gap" - OCR extracts symbols, Parser understands intent.
    """
    
    def parse(self, ocr_output: Dict | str) -> Dict:
        """
        Parse problem from OCR output.
        
        Args:
            ocr_output: Dict from MathOCR with 'problem_data' key OR raw string
            
        Returns:
            Dict with:
                - 'problem_statement': Full problem in natural language
                - 'question': What needs to be found/calculated
                - 'given': Dict of known values
                - 'domain': Problem type (algebra, calculus, etc.)
                - 'approach': Suggested solution strategy
                - 'confidence': How confident the parser is
                - 'error': Error message if parsing failed
        """
        # Handle string input (from direct text entry)
        if isinstance(ocr_output, str):
             ocr_output = {"latex": ocr_output}

        # Extract problem data from OCR
        problem_data = ocr_output.get("problem_data", {})
        
        # If OCR already structured it, use that as base
        if isinstance(problem_data, dict) and "problem_text_full" in problem_data:
            problem_text = problem_data["problem_text_full"]
            given_values = problem_data.get("given_values", [])
            question_hint = problem_data.get("question", "")
            domain_hint = problem_data.get("problem_type_hint", "")
        else:
            # Fallback: use raw latex
            problem_text = ocr_output.get("latex", "")
            given_values = []
            question_hint = ""
            domain_hint = ""
        
        # Build parsing prompt
        prompt =self._build_parse_prompt(problem_text, given_values, question_hint, domain_hint)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            parsed = self._extract_parsed_data(response.text)
            
            return {
                "problem_statement": parsed.get("problem_statement", problem_text),
                "question": parsed.get("question", question_hint),
                "domain": parsed.get("domain", domain_hint),
                "approach": parsed.get("approach", ""),
                "needs_clarification": parsed.get("question", "Unknown") == "Unknown",
                "error": None
            }
        except Exception as e:
            return {
                "problem_statement": problem_text,
                "question": question_hint,
                "domain": domain_hint,
                "approach": "",
                "error": str(e)
            }
    
    def _build_parse_prompt(self, problem_text: str, given_values: list, question_hint: str, domain_hint: str) -> str:
        """Build prompt for parsing."""
        return f"""You are a math problem parser. Extract key information from the problem.

**Problem Text**:
{problem_text}

**Your Task**: Extract the following as JSON:

1. **problem_statement**: Rephrase the problem clearly and completely
2. **question**: What exactly needs to be found? (e.g., "Find P(T)", "Solve for x")
3. **domain**: Problem type ("algebra", "calculus", "probability", "geometry", etc.)
4. **approach**: High-level solution strategy (e.g., "Use probability union formula", "Apply quadratic formula")

**Output JSON only**:
{{
  "problem_statement": "...",
  "question": "...",
  "domain": "...",
  "approach": "..."
}}

**Examples**:

Problem: "Solve x² + 3x - 4 = 0 for x"
Output:
{{
  "problem_statement": "Solve the quadratic equation x² + 3x - 4 = 0",
  "question": "Find the value(s) of x",
  "domain": "algebra",
  "approach": "Apply quadratic formula or factorization"
}}

Problem: "Three students with success probabilities 1/3, 1/10, 1/12. Find P(at least one solves)"
Output:
{{
  "problem_statement": "Three students S₁, S₂, S₃ attempt a problem with individual success probabilities 1/3, 1/10, and 1/12 respectively. Find the probability that at least one student solves it.",
  "question": "Find P(at least one student succeeds)",
  "domain": "probability",
  "approach": "Calculate probability of complement (none succeed), then subtract from 1"
}}

Now parse the given problem.
"""
    
    def _extract_parsed_data(self, response_text: str) -> Dict:
        """Extract JSON from Gemini response."""
        import json
        
        try:
            # Remove markdown
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback: return empty structure
            return {
                "problem_statement": response_text,
                "question": "Unknown",
                "domain": "unknown",
                "approach": ""
            }
    
    def is_math_related(self, text: str) -> Dict:
        """
        Check if the input is a math-related question using LLM classification.
        
        Fully dynamic - no hardcoded keywords. Handles edge cases like:
        - Proof requests
        - Theory/concept explanations
        - Mathematical history
        
        Returns:
            Dict with 'is_math': bool, 'reason': str
        """
        try:
            prompt = f"""You are a guardrail classifier for a MATH TUTORING application.

**User Input:**
{text[:1000]}

**Classify as MATH if the user is asking about ANY of these:**
- Solving equations, problems, or calculations
- Mathematical proofs or derivations
- Mathematical concepts, theorems, or theory
- Mathematical definitions or explanations
- Geometry, algebra, calculus, probability, statistics, etc.
- Numbers, formulas, functions, graphs
- Mathematical reasoning or logic

**Classify as NOT_MATH if the user is asking about:**
- General conversation or greetings
- Non-mathematical topics (history, entertainment, cooking, etc.)
- Personal advice or opinions
- Programming (unless it's about mathematical algorithms)
- Other subjects unrelated to mathematics

**Respond with EXACTLY one of these:**
- MATH (if related to mathematics in any way)
- NOT_MATH (if clearly unrelated to mathematics)
"""
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            answer = response.text.strip().upper()
            
            is_math = "MATH" in answer and "NOT_MATH" not in answer
            return {
                "is_math": is_math,
                "reason": answer.replace("MATH", "").replace("_", " ").strip() or ("Mathematics-related" if is_math else "Not mathematics-related")
            }
        except Exception as e:
            # On error, allow through (fail open)
            return {"is_math": True, "reason": f"Classification failed ({e}), allowing through"}


if __name__ == "__main__":
    # Test parser
    parser = ParserAgent()
    
    # Test case: Simple algebra
    test_ocr = {
        "problem_data": {
            "problem_text_full": "Solve x² + 3x - 4 = 0 for x",
            "given_values": ["x² + 3x - 4 = 0"],
            "question": "Solve for x",
            "problem_type_hint": "algebra"
        },
        "confidence": 0.9
    }
    
    result = parser.parse(test_ocr)
    print("Parsed Result:")
    print(f"Question: {result['question']}")
    print(f"Domain: {result['domain']}")
    print(f"Approach: {result['approach']}")
    print(f"Confidence: {result['confidence']:.0%}")
