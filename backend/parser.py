"""
Parser Agent - Understands math problems and structures them for solving.
Bridges the gap between OCR (raw text) and Solver (code generation).
"""

from google import genai
import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class ParserAgent:
    """
    Understands math problems and extracts actionable information.
    
    Input: OCR output (full problem text)
    Output: Structured problem representation
    
    This solves the "context gap" - OCR extracts symbols, Parser understands intent.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize Parser Agent."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
    
    def parse(self, ocr_output: Dict) -> Dict:
        """
        Parse problem from OCR output.
        
        Args:
            ocr_output: Dict from MathOCR with 'problem_data' key
            
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
                "given": parsed.get("given", {}),
                "domain": parsed.get("domain", domain_hint),
                "approach": parsed.get("approach", ""),
                "relationships": parsed.get("relationships", []),
                "confidence": self._calculate_confidence(parsed),
                "error": None
            }
        except Exception as e:
            return {
                "problem_statement": problem_text,
                "question": question_hint,
                "given": {},
                "domain": domain_hint,
                "approach": "",
                "relationships": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _build_parse_prompt(self, problem_text: str, given_values: list, question_hint: str, domain_hint: str) -> str:
        """Build prompt for parsing."""
        return f"""You are a math problem parser. Your job is to UNDERSTAND the problem and extract key information.

**Problem Text**:
{problem_text}

**Hints**:
- Given values: {given_values}
- Question: {question_hint}
- Domain: {domain_hint}

**Your Task**: Extract the following information as JSON:

1. **problem_statement**: Rephrase the problem in clear, complete sentences
2. **question**: What exactly needs to be found/calculated? (e.g., "Find P(T)", "Solve for x")
3. **given**: Dictionary of known values (e.g., {{"x": "5", "y": "10", "P_U": "1/3"}})
4. **domain**: Problem type ("algebra", "calculus", "probability", "geometry", etc.)
5. **relationships**: List of formulas or rules that connect given to asked (e.g., ["P(A ∪ B) = P(A) + P(B) - P(A ∩ B)"])
6. **approach**: High-level solution strategy (e.g., "Use probability union formula", "Apply quadratic formula")

**Output JSON only**:
{{
  "problem_statement": "...",
  "question": "...",
  "given": {{}},
  "domain": "...",
  "relationships": [],
  "approach": "..."
}}

**Examples**:

Problem: "Solve x² + 3x - 4 = 0 for x"
Output:
{{
  "problem_statement": "Solve the quadratic equation x² + 3x - 4 = 0",
  "question": "Find the value(s) of x",
  "given": {{"equation": "x² + 3x - 4 = 0"}},
  "domain": "algebra",
  "relationships": ["Quadratic formula: x = (-b ± √(b²-4ac)) / 2a"],
  "approach": "Apply quadratic formula or factorization"
}}

Problem: "Three students with success probabilities 1/3, 1/10, 1/12. Find P(at least one solves)"
Output:
{{
  "problem_statement": "Three students S₁, S₂, S₃ attempt a problem with individual success probabilities 1/3, 1/10, and 1/12 respectively. Find the probability that at least one student solves it.",
  "question": "Find P(at least one student succeeds)",
  "given": {{"P_S1": "1/3", "P_S2": "1/10", "P_S3": "1/12"}},
  "domain": "probability",
  "relationships": ["P(at least one) = 1 - P(none)", "P(none) = (1-P_S1)(1-P_S2)(1-P_S3)"],
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
                "given": {},
                "domain": "unknown",
                "relationships": [],
                "approach": ""
            }
    
    def _calculate_confidence(self, parsed_data: Dict) -> float:
        """Calculate confidence in parsing."""
        confidence = 0.5  # Base
        
        # Has clear question (+0.2)
        if parsed_data.get("question") and parsed_data["question"] != "Unknown":
            confidence += 0.2
        
        # Has given values (+0.1)
        if parsed_data.get("given") and len(parsed_data["given"]) > 0:
            confidence += 0.1
        
        # Has domain (+0.1)
        if parsed_data.get("domain") and parsed_data["domain"] != "unknown":
            confidence += 0.1
        
        # Has approach (+0.1)
        if parsed_data.get("approach"):
            confidence += 0.1
        
        return min(confidence, 1.0)


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
