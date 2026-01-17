"""
Solver Agent - Generates SymPy code from natural language math problems.
Uses Gemini 2.0 Flash API with Program-of-Thoughts (PoT) pattern.
"""

from google import genai
import re
from typing import Dict, Optional
try:
    from .config import config
except ImportError:
    from config import config


class SolverAgent:
    """
    Generates executable Python code using SymPy to solve math problems.
    
    The agent does NOT compute answers directly - it only writes code.
    This follows the Program-of-Thoughts (PoT) pattern:
    - LLM = "planner" (decides strategy)
    - SymPy = "executor" (performs deterministic computation)
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the Solver Agent with BEST reasoning model.
        
        Args:
            model_name: Gemini model (uses config default if not specified)
        """
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = model_name or config.GEMINI_MODEL
        
    def solve(self, problem: str) -> Dict[str, str]:
        """
        Generate SymPy code to solve a math problem.
        
        Args:
            problem: Natural language math problem
            
        Returns:
            Dict with:
                - 'code': Generated Python code
                - 'reasoning': Model's thought process (if available)
                - 'error': Error message if generation failed
        """
        prompt = self._build_prompt(problem)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            code = self._extract_code(response.text)
            
            return {
                "code": code,
                "reasoning": response.text.split("```python")[0].strip() if "```python" in response.text else "",
                "error": None
            }
        except Exception as e:
            return {
                "code": None,
                "reasoning": None,
                "error": str(e)
            }
    
    def solve_from_parsed(self, parsed_problem: Dict) -> Dict[str, str]:
        """
        Generate SymPy code from PARSED problem (with context).
        
        Args:
            parsed_problem: Dict from ParserAgent with structured information
            
        Returns:
            Same as solve() but with better context-aware code generation
        """
        prompt = self._build_contextual_prompt(parsed_problem)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            code = self._extract_code(response.text)
            
            return {
                "code": code,
                "reasoning": response.text.split("```python")[0].strip() if "```python" in response.text else "",
                "error": None
            }
        except Exception as e:
            return {
                "code": None,
                "reasoning": None,
                "error": str(e)
            }
    
    def _build_contextual_prompt(self, parsed_problem: Dict) -> str:
        """Build enhanced prompt from parsed problem structure."""
        problem_stmt = parsed_problem.get("problem_statement", "")
        question = parsed_problem.get("question", "")
        given = parsed_problem.get("given", {})
        relationships = parsed_problem.get("relationships", [])
        approach = parsed_problem.get("approach", "")
        
        # Format given values
        given_str = "\n".join([f"- {k} = {v}" for k, v in given.items()])
        
        # Format relationships
        rel_str = "\n".join([f"- {r}" for r in relationships])
        
        try:
            from prompts import get_prompt
            template = get_prompt("solver_contextual")
            return template.format(
                problem_statement=problem_stmt,
                question=question,
                given_values=given_str if given_str else "None explicitly given",
                relationships=rel_str if rel_str else "Derive from problem context",
                approach=approach if approach else "Determine from problem type"
            )
        except Exception:
            # Fallback to minimal inline prompt
            return f"""You are a mathematical tutor. Solve this problem step by step.

**Problem**: {problem_stmt}
**Question**: {question}
**Given**: {given_str if given_str else "See problem"}
**Approach**: {approach if approach else "Determine best method"}

Provide: INTUITION, SOLUTION STEPS, CODE (with `answer = ...`), EXPLANATION.
"""
    
    def _build_prompt(self, problem: str) -> str:
        """
        Build the prompt for code generation.
        
        Critical design choices:
        1. Forbid the LLM from calculating directly
        2. Require storing final answer in `answer` variable
        3. Provide examples to guide output format
        """
        try:
            from prompts import get_prompt
            template = get_prompt("solver_basic")
            return template.format(problem=problem)
        except Exception:
            # Fallback to inline prompt if file loading fails
            return f"""You are a math problem solver that generates ONLY executable Python code using SymPy.

**Problem**: {problem}

**Rules**:
1. Import everything from sympy: `from sympy import *`
2. Solve the problem symbolically using SymPy functions
3. Store the final answer in a variable named `answer`
4. Do NOT compute manually - let SymPy do all calculations
5. Output ONLY the code - no explanations before or after

Now generate code for the given problem. Output ONLY the Python code inside ```python``` tags.
"""

    def _extract_code(self, response_text: str) -> Optional[str]:
        """
        Extract Python code from the LLM response.
        
        Handles formats:
        - ```python ... ```
        - ```\n ... \n```
        - Plain code (no markers)
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
        
        # Assume entire response is code (fallback)
        return response_text.strip()


if __name__ == "__main__":
    # Test the solver
    solver = SolverAgent()
    
    test_problems = [
        "Solve x**2 + 3x - 4 = 0 for x",
        "Integrate x**3 from 0 to 5",
        "Find the derivative of e**x * sin(x)"
    ]
    
    for problem in test_problems:
        print(f"\n{'='*60}")
        print(f"Problem: {problem}")
        print(f"{'='*60}")
        
        result = solver.solve(problem)
        
        if result["error"]:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"Generated Code:\n{result['code']}")
