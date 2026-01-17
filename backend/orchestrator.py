"""
Orchestrator - The "Manager" that wires all agents together.
Implements the 'Reflexion' pattern for self-correcting problem solving.
"""

import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import re

# Import text processing utilities
try:
    from utils.text_utils import strip_code_from_reasoning
except ImportError:
    # Fallback for standalone execution
    import re
    def strip_code_from_reasoning(reasoning):
        if not isinstance(reasoning, str) or reasoning is None:
            return ''
        reasoning = re.sub(r'\*\*Internal Code\*\*.*', '', reasoning, flags=re.DOTALL | re.IGNORECASE)
        reasoning = re.sub(r'```[^`]*```', '', reasoning, flags=re.DOTALL)
        return reasoning.strip()

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from agents.parser import ParserAgent
from agents.router import RouterAgent
from agents.solver import SolverAgent
from agents.verifier import VerifierAgent
from schemas import ParsedProblem, RouteDecision, Solution, Verification

@dataclass
class Attempt:
    """A single attempt to solve the problem."""
    round: int
    solution: Dict[str, Any]  # Code, Reasoning
    verification: Verification
    reflection: Optional[str] = None  # Why it failed + what to do next

@dataclass
class PipelineContext:
    """State object flowing through the pipeline."""
    raw_input: str
    parsed: Optional[ParsedProblem] = None
    route: Optional[RouteDecision] = None
    rag_context: str = ""
    attempts: List[Attempt] = field(default_factory=list)
    final_solution: Optional[Dict[str, Any]] = None
    status: str = "init"  # init, solving, verified, failed

class Orchestrator:
    """
    Coordinates the Multi-Agent System.
    Flow: Parser -> Router -> RAG -> Solver -> Verifier -> (Reflector Loop).
    """
    
    def __init__(self, parser=None, router=None, solver=None, verifier=None, max_retries=3):
        """
        Initialize Orchestrator with dependency injection support.
        
        Args:
            parser: ParserAgent instance (or None to use default)
            router: RouterAgent instance (or None to use default)
            solver: SolverAgent instance (or None to use default)
            verifier: VerifierAgent instance (or None to use default)
            max_retries: Maximum reflexion attempts (default: 3)
        """
        # Dependency Injection with sensible defaults
        self.parser = parser or ParserAgent()
        self.router = router or RouterAgent()
        self.solver = solver or SolverAgent()
        self.verifier = verifier or VerifierAgent()
        self.max_retries = max_retries
        
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Run the full SOTA math solving pipeline.
        
        Args:
            user_input: The math problem (text).
            
        Returns:
            Dict containing final response, events, and debug info.
        """
        # 0. Check for Follow-up / Conversational Intent
        # We leverage the Solver's memory to detect context
        self.solver.memory.add_user_message(user_input)
        is_follow_up = self.solver.memory.is_follow_up(user_input)
        
        if is_follow_up:
            response = self.solver._generate_follow_up_response(user_input)
            self.solver.memory.add_assistant_message(response)
            return {
                "response": response,
                "events": ["Detected follow-up question", "Generated conversational response"],
                "context": None
            }

        # Be sure to set this as the active problem for context
        self.solver.memory.set_active_problem(user_input)

        ctx = PipelineContext(raw_input=user_input)
        events = []  # Log of what happened (for UI)
        
        # 1. Parse
        events.append("Parsing problem...")
        parsed_dict = self.parser.parse(user_input)
        
        # Convert Dict to ParsedProblem Object
        ctx.parsed = ParsedProblem(
            problem_text=parsed_dict.get("problem_statement", ""),
            topic=parsed_dict.get("domain", "unknown"),
            question=parsed_dict.get("question", ""),
            approach=parsed_dict.get("approach", ""),
            needs_clarification=parsed_dict.get("needs_clarification", False)
        )
        
        if ctx.parsed.needs_clarification:
            return {
                "response": f"I need clarification: {ctx.parsed.problem_text}",
                "status": "clarification_needed"
            }
        # 2. Route
        events.append("Routing to domain specialist...")
        for i in range(self.max_retries):
            events.append(f"Attempt {i+1}/{self.max_retries}...")
            
            # A. Solve
            # If this is a retry, inject reflection history
            context_prompt = None
            problem_for_solver = ctx.parsed.problem_text
            
            if i > 0:
                history = self._format_history(ctx.attempts)
                problem_for_solver += f"\n\n[PREVIOUS ATTEMPTS FAILED]\nADJUST STRATEGY based on history:\n{history}"
            
            solution = self.solver.solve(problem_for_solver)
            
            # Record RAG context if it's the first attempt
            if i == 0 and solution.get('rag_context'):
                ctx.rag_context = solution['rag_context']
                # Create a concise preview for the UI
                preview = solution['rag_context'].split('\n')[0][:80] + "..."
                events.append(f"📚 RAG Retrieved: {preview}")

            if solution['error']:
                events.append(f"Solver Error: {solution['error']}")
                ctx.attempts.append(Attempt(
                    round=i,
                    solution={**solution, "answer": "Generation Failed"},
                    verification=Verification(is_valid=False, confidence=0, issues=[str(solution['error'])]),
                    reflection="Solver crashed. Check syntax."
                ))
                continue
                
            # B. Verify
            events.append("Verifying solution...")
            
            # Use Verifier's executor to run the solution code to get the answer
            exec_result = self.verifier.executor.execute(solution['code'])
            
            if not exec_result['success']:
                # Execution failed
                verification = Verification(
                    is_valid=False, 
                    confidence=0, 
                    issues=[f"Runtime Error: {exec_result['error']}"],
                    checks_performed=[]
                )
                answer_val = "Error"
            else:
                answer_val = str(exec_result['answer'])
                # Verify the result logic
                verification = self.verifier.verify(
                    ctx.parsed.problem_text,
                    solution['code'],
                    answer_val
                )
            
            # Record Attempt
            attempt = Attempt(
                round=i,
                solution={**solution, "answer": answer_val},
                verification=verification
            )
            
            # C. Check Success
            if verification.is_valid:
                ctx.final_solution = attempt.solution
                ctx.status = "verified"
                events.append("✅ Verification Passed!")
                ctx.attempts.append(attempt)
                break
            else:
                events.append(f"❌ Verification Failed: {verification.issues}")
                
                # D. Reflect
                reflection_prompt = f"""
                I tried to solve: "{ctx.parsed.problem_text}"
                My Code: \n{solution['code']}\n
                Result: {answer_val}
                Verifier Feedback: {verification.issues}
                
                Why did this fail? What should I do differently next time?
                Be concise. Focus on fixing the specific error.
                """
                
                try:
                    reflection = self.solver.client.models.generate_content(
                        model=self.solver.model_name,
                        contents=reflection_prompt
                    ).text
                except:
                    reflection = "Try a different approach."
                
                attempt.reflection = reflection
                events.append(f"🤔 Reflection: {reflection}")
                ctx.attempts.append(attempt)
        
        # 5. Final Output Generation
        msg = ""
        if ctx.status == "verified":
            # Strip the entire "Internal Code" section from reasoning
            reasoning = strip_code_from_reasoning(ctx.final_solution.get('reasoning'))
            
            msg = f"### Solution\n\n{reasoning}\n\n**Answer:** {ctx.final_solution['answer']}\n\n"
            if len(ctx.attempts) > 1:
                msg += f"*Verified in {len(ctx.attempts)} attempts (Reflexion Active).*"
        else:
            msg = f"### Solution (Unverified)\n\nI struggled to verify the answer. Here is my best attempt:\n\n"
            if ctx.attempts:
                last = ctx.attempts[-1]
                
                # Strip code section from reasoning
                reasoning = last.solution.get('reasoning', 'No reasoning available')
                reasoning = strip_code_from_reasoning(reasoning)
                if not reasoning:
                    reasoning = 'No reasoning available'
                
                msg += f"{reasoning}\n\n**Possible Answer:** {last.solution.get('answer', 'Unknown')}\n"
                msg += f"\n*Issues found:* {last.verification.issues}"
        
        # Save solution to memory
        self.solver.memory.add_assistant_message(msg)
        
        # Generator Visual Deck (If verified)
        deck = None
        if ctx.status == "verified" and ctx.final_solution:
            try:
                events.append("Generating visual explanation...")
                deck = self.solver.solve_structured(
                    ctx.parsed.problem_text, 
                    context={"approach": ctx.final_solution.get("reasoning", "")}
                )
            except Exception as e:
                events.append(f"Visual generation failed: {e}")

        return {
            "response": msg,
            "events": events,
            "context": ctx,
            "deck": deck
        }

    def _format_history(self, attempts: List[Attempt]) -> str:
        """Format reflexion history for display."""
        if len(attempts) <= 1:
            return ""
        return f"\n\n---\n**Reflexion History:**\n- {len(attempts)} attempts\n- Final solution verified ✓"
    
    # Facade methods for cleaner frontend access
    def add_user_message(self, content: str):
        """Facade: Add user message to conversation memory."""
        self.solver.memory.add_user_message(content)
    
    def add_assistant_message(self, content: str, deck=None):
        """Facade: Add assistant message to conversation memory."""
        self.solver.memory.add_assistant_message(content, deck)
    
    def restore_session(self) -> bool:
        """Facade: Restore last conversation session."""
        return self.solver.memory.restore_last_session()
    
    def clear_conversation(self):
        """Facade: Clear conversation history."""
        self.solver.memory.clear()
    
    def get_conversation_context(self, limit: int = 5) -> str:
        """Facade: Get recent conversation context."""
        return self.solver.memory.get_context_window(limit)
