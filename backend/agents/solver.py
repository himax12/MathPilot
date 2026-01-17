"""
Solver Agent - Generates SymPy code from natural language math problems.
Uses Gemini 2.0 Flash API with Program-of-Thoughts (PoT) pattern.
"""

from google import genai
import re
from typing import Dict, Optional
import sys
import os

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from config import config
from deck_generator.models import MathDeck, MathSlide, VisualRequest
from memory import ConversationMemory
from knowledge import MathRAG


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
        
        # Store API key and cache client instance
        self._api_key = config.GEMINI_API_KEY
        self._client_instance = None
        self.model_name = model_name or config.GEMINI_MODEL
        self.memory = ConversationMemory()  # Multi-turn conversation state
        self.rag = MathRAG()  # Initialize RAG engine
    
    @property
    def client(self):
        """Lazy-init and cache client to avoid both event loop AND garbage collection issues."""
        if self._client_instance is None:
            self._client_instance = genai.Client(api_key=self._api_key)
        return self._client_instance
    
    def chat(self, user_input: str) -> Dict[str, any]:
        """
        Multi-turn chat interface. Handles both new problems and follow-ups.
        
        Args:
            user_input: User's message (could be a problem or a follow-up)
            
        Returns:
            Dict with: 'response' (text), 'deck' (optional MathDeck), 'is_new_problem' (bool)
        """
        # Add user message to memory
        self.memory.add_user_message(user_input)
        
        # Determine if this is a follow-up or a new problem
        is_follow_up = self.memory.is_follow_up(user_input)
        
        if is_follow_up:
            # Generate a contextual response using conversation history
            response = self._generate_follow_up_response(user_input)
            self.memory.add_assistant_message(response)
            return {
                "response": response,
                "deck": None,
                "is_new_problem": False
            }
        else:
            # Treat as a new problem - use text-based solve for reliability
            self.memory.set_active_problem(user_input)
            
            result = self.solve(user_input)
            
            if result.get("error"):
                error_msg = f"I encountered an issue: {result['error']}"
                self.memory.add_assistant_message(error_msg)
                return {"response": error_msg, "deck": None, "is_new_problem": True}
            
            reasoning = result.get("reasoning", "")
            code = result.get("code", "")
            
            # Build a comprehensive response
            response_parts = []
            if reasoning:
                response_parts.append(reasoning)
            if code:
                response_parts.append(f"\n**Generated Code:**\n```python\n{code}\n```")
            
            response = "\n".join(response_parts) if response_parts else "I processed your request."
            
            self.memory.add_assistant_message(response)
            return {
                "response": response,
                "deck": None,  # Skip deck for now until schema issues resolved
                "is_new_problem": True,
                "code": code
            }
    
    def _generate_follow_up_response(self, user_input: str) -> str:
        """Generate a response to a follow-up question using context."""
        context = self.memory.get_context_window(limit=5)
        
        prompt = f"""
You are a friendly Math Mentor continuing a conversation.

{context}

[NEW USER MESSAGE]:
{user_input}

**INSTRUCTIONS**:
- You ALREADY solved the problem shown in the context.
- Answer the user's follow-up question based on that solution.
- Be concise but educational.
- If they ask "why", explain the reasoning.
- If they ask about a specific step, reference it.
- Use Markdown for formatting.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"I had trouble answering that: {e}"
    
    def reset_conversation(self) -> None:
        """Clear conversation history for a fresh start."""
        self.memory.clear()
        
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

        
        # RAG Retrieval
        rag_context = ""
        if self.rag.ready:
            rag_context = self.rag.retrieve(problem)

        prompt = self._build_prompt(problem, rag_context)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            code = self._extract_code(response.text)
            
            return {
                "code": code,
                "reasoning": response.text.split("```python")[0].strip() if "```python" in response.text else "",
                "error": None,
                "rag_context": rag_context
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
    
    
    def solve_structured(self, problem: str, context: Optional[Dict] = None) -> Optional[MathDeck]:
        """
        Generate a structured MathDeck using Gemini's native JSON schema enforcement.
        
        Args:
            problem: Natural language math problem
            context: Optional dictionary with parsed approach/context
            
        Returns:
            MathDeck object or None if generation fails
        """
        prompt = self._build_structured_prompt(problem, context)
        
        try:
            # Use Gemini 2.0's strict structured output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': MathDeck,
                }
            )
            
            # The SDK automatically validates matches against the schema
            # We just need to parse the JSON into our Pydantic model
            return response.parsed
            
        except Exception as e:
            print(f"Error generating structured deck: {e}")
            return None

    def _build_structured_prompt(self, problem: str, context: Optional[Dict] = None) -> str:
        """Build prompt specifically for Deck generation."""
        base_prompt = f"""
You are a Math Tutor creating an interactive visual explanation deck.

**OBJECTIVE**: 
Create a clear, step-by-step explanation for: "{problem}"

**GUIDELINES**:
1. **Structure**: Break it down into INTUITION (why), STEPS (how), and VISUALIZATION.
2. **Visuals**: PROACTIVELY request diagrams.
   - If Algebra: Request 'parabola', 'coordinate_plane', or 'number_line'.
   - If Geometry: Request 'triangle', 'unit_circle', etc.
   - CALCULATE exact parameters for the diagram (e.g., vertex `a`, `b`, `c`).
3. **Tone**: Educational, encouraging, clear.
4. **Formatting**: Use Markdown for content, but NO code blocks for the output itself (it must be JSON).

**Visual Request Examples**:
- asking for a parabola y = x^2: `type="parabola", params={{"a": 1, "b": 0, "c": 0}}`
- asking for a triangle: `type="triangle", params={{"vertices": [[0,0], [3,0], [0,4]], "labels": ["A", "B", "C"]}}`
"""
        if context:
             base_prompt += f"\n**Context/Approach**: {context.get('approach', 'Standard method')}"
             
        return base_prompt

    def _build_prompt(self, problem: str, rag_context: str = "") -> str:
        """
        Build the prompt for code generation.
        
        Critical design choices:
        1. Forbid the LLM from calculating directly
        2. Require storing final answer in `answer` variable
        3. Provide examples to guide output format
        """
        full_problem = problem
        if rag_context:
            full_problem = f"{problem}\n\n[RELEVANT MATH KNOWLEDGE]\n{rag_context}"
            
        try:
            from prompts import get_prompt
            template = get_prompt("solver_basic")
            return template.format(problem=full_problem)
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
