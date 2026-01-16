"""
Solver Agent - Generates SymPy code from natural language math problems.
Uses Gemini 2.0 Flash API with Program-of-Thoughts (PoT) pattern.
"""

from google import genai
import os
import re
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class SolverAgent:
    """
    Generates executable Python code using SymPy to solve math problems.
    
    The agent does NOT compute answers directly - it only writes code.
    This follows the Program-of-Thoughts (PoT) pattern:
    - LLM = "planner" (decides strategy)
    - SymPy = "executor" (performs deterministic computation)
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the Solver Agent with BEST reasoning model.
        
        Args:
            model_name: Gemini model (default: gemini-2.0-flash-exp)
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        
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
        
        return f"""You are a mathematical tutor using Gemini 2.0 Flash Thinking.

**YOUR ROLE**: Teach math beautifully! Show mathematical reasoning, NOT programming.

**CRITICAL INSTRUCTIONS**:
1. Provide INTUITIVE EXPLANATION in simple terms
2. Show MATHEMATICAL SOLUTION STEPS (use proper math notation)
3. Generate executable Python code (hidden from user, just for calculation)
4. Provide clean EXPLANATION with final answer interpretation

**Problem Statement**: {problem_stmt}

**Question**: {question}

**Given Values**:
{given_str if given_str else "None explicitly given"}

**Relevant Formulas**:
{rel_str if rel_str else "Derive from problem context"}

**Suggested Approach**: {approach if approach else "Determine from problem type"}

**CRITICAL OUTPUT FORMATTING RULES**:

1. **NO UNICODE MATH**: Use plain text (x^2 not ², sqrt() not √)
2. **ONE STEP PER LINE**: Clear breaks between steps
3. **BOLD KEY VALUES**: Use **bold** for important numbers
4. **NO IMPORTS**: `sympy`, `numpy` (as `np`), and `matplotlib.pyplot` (as `plt`) are PRE-LOADED. Do not import them.

**OUTPUT FORMAT**:

**INTUITION**:
[Brief explanation in plain English - why this approach works]

**SOLUTION STEPS**:

**Step 1**: [First action]
- ...

**VISUALIZATION** (if helpful):
```python
# Libraries `plt` and `np` are PRE-LOADED. Do not import.
# Create explanatory visualization
fig, ax = plt.subplots(...)
...
plt.savefig('explanation_viz.png', dpi=150, bbox_inches='tight')
plt.close()
```

**CODE** (calculation):
```python
# `sympy` is PRE-LOADED. Do not import.
# Calculation here
answer = ...
```

**EXPLANATION**:
[Interpretation]

---

Now solve with CLEAN, STEP-BY-STEP formatting.
"""
    
    def _build_prompt(self, problem: str) -> str:
        """
        Build the prompt for code generation.
        
        Critical design choices:
        1. Forbid the LLM from calculating directly
        2. Require storing final answer in `answer` variable
        3. Provide examples to guide output format
        """
        return f"""You are a math problem solver that generates ONLY executable Python code using SymPy.

**Problem**: {problem}

**Rules**:
1. Import everything from sympy: `from sympy import *`
2. Solve the problem symbolically using SymPy functions
3. Store the final answer in a variable named `answer`
4. Do NOT compute manually - let SymPy do all calculations
5. Output ONLY the code - no explanations before or after

**Example 1**:
Problem: Solve x**2 - 4 = 0 for x
Code:
```python
from sympy import *
x = symbols('x')
equation = Eq(x**2 - 4, 0)
answer = solve(equation, x)
```

**Example 2**:
Problem: Integrate x**2 from 0 to 10
Code:
```python
from sympy import *
x = symbols('x')
answer = integrate(x**2, (x, 0, 10))
```

**Example 3**:
Problem: Find the derivative of sin(x) * cos(x)
Code:
```python
from sympy import *
x = symbols('x')
expr = sin(x) * cos(x)
answer = diff(expr, x)
```

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
