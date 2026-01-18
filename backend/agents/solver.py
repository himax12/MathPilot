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
from agents.base import BaseAgent

# Import utilities
try:
    from utils.text_utils import extract_code_from_response
except ImportError:
    import re
    def extract_code_from_response(response_text):
        pattern = r"```python\s*(.*?)\s*```"
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        pattern = r"```\s*(.*?)\s*```"
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()


class SolverAgent(BaseAgent):
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
        super().__init__(model_name)
        self.memory = ConversationMemory()  # Multi-turn conversation state
        self._rag_instance = None  # Lazy-load RAG
    
    @property
    def rag(self):
        """Lazy-load RAG only when needed (saves 200-500ms on startup)."""
        if self._rag_instance is None:
            self._rag_instance = MathRAG()
        return self._rag_instance
    
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

        # Episodic Memory Retrieval (Self-Learning)
        memory_context = ""
        try:
            # We look for similar past problems to see how we solved them
            memory_context = self.memory.search_memories(problem, top_k=2)
        except Exception:
            pass

        prompt = self._build_prompt(problem, rag_context, memory_context)
        
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

    def _build_prompt(self, problem: str, rag_context: str = "", memory_context: str = "") -> str:
        """
        Build the prompt for code generation.
        
        Critical design choices:
        1. Forbid the LLM from calculating directly
        2. Require storing final answer in `answer` variable
        3. Provide examples to guide output format
        """
        full_problem = problem
        if rag_context:
            full_problem += f"\n\n[RELEVANT MATH KNOWLEDGE]\n{rag_context}"
        
        if memory_context:
            full_problem += f"\n\n[PAST EXPERIENCE / SIMILAR PROBLEMS]\nUse this history to avoid previous mistakes:\n{memory_context}"
            
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
        Uses centralized utility function.
        """
        return extract_code_from_response(response_text)
