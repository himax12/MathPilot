"""
Solver Agent - Generates SymPy code from natural language math problems.
Uses Gemini 2.0 Flash API with Program-of-Thoughts (PoT) pattern.
"""

from google import genai
import re
from typing import Dict, Optional

from backend.config import config
from backend.deck_generator.models import MathDeck, MathSlide, VisualRequest
from backend.memory import ConversationMemory
from backend.knowledge import MathRAG
from backend.agents.base import BaseAgent
from backend.utils.text_utils import extract_code_from_response


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
        Generate SymPy code to solve a math problem using two-tier RAG strategy.
        
        Strategy:
        - High similarity (>=0.6): Use KB-guided prompt emphasizing knowledge base solutions
        - Low similarity (<0.6): Use standard LLM-only prompt
        
        Args:
            problem: Natural language math problem
            
        Returns:
            Dict with 'code', 'reasoning', 'error', 'rag_context', 'solving_mode'
        """
        
        # TWO-TIER RAG: Get context WITH similarity score
        rag_result = {"context": "", "max_similarity": 0.0, "has_strong_match": False, "top_topic": ""}
        if self.rag.ready:
            rag_result = self.rag.retrieve_with_score(problem)
        
        rag_context = rag_result.get("context", "")
        has_strong_match = rag_result.get("has_strong_match", False)
        max_similarity = rag_result.get("max_similarity", 0.0)
        top_topic = rag_result.get("top_topic", "")

        # Episodic Memory Retrieval (Self-Learning)
        memory_context = ""
        try:
            memory_context = self.memory.search_memories(problem, top_k=2)
        except Exception:
            pass

        # Choose prompt strategy based on RAG match quality
        if has_strong_match and rag_context:
            # HIGH SIMILARITY: KB-guided solving (trust the knowledge base)
            solving_mode = f"KB-Guided ({top_topic}, {max_similarity:.0%} match)"
            prompt = self._build_kb_guided_prompt(problem, rag_context, memory_context)
        else:
            # LOW SIMILARITY: Standard LLM-only solving
            solving_mode = f"LLM-Only (best KB match: {max_similarity:.0%})"
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
                "rag_context": rag_context,
                "solving_mode": solving_mode
            }
        except Exception as e:
            return {
                "code": None,
                "reasoning": None,
                "error": str(e),
                "solving_mode": solving_mode
            }
    
    def _build_kb_guided_prompt(self, problem: str, rag_context: str, memory_context: str = "") -> str:
        """
        Build prompt for KB-guided solving (high similarity match).
        
        Instead of injecting raw KB content (which can confuse code generation),
        we tell the LLM that a matching topic was found and let it use its training.
        """
        # Extract just the topic names from RAG context for guidance
        topic_hint = ""
        if "Source 1:" in rag_context:
            # Extract topic from first source header
            import re
            match = re.search(r"Source \d+:\s*([^\(]+)", rag_context)
            if match:
                topic_hint = match.group(1).strip()
        
        prompt = f"""You are a Math Tutor. Solve this problem using SymPy.

**TOPIC HINT:** This problem is related to: {topic_hint if topic_hint else "mathematics"}

**PROBLEM:**
{problem}

**INSTRUCTIONS:**
1. Write Python code using SymPy to solve this problem.
2. Store the final answer in a variable named `answer`.
3. Use appropriate SymPy functions (simplify, solve, integrate, etc.).
4. The code should be complete and executable.

**Output ONLY the Python code inside ```python``` tags.**
"""
        if memory_context:
            prompt += f"\n\n**Past Experience:**\n{memory_context}"
        
        return prompt
    
    
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
