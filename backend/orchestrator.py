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

from backend.utils.text_utils import strip_code_from_reasoning
from backend.agents.parser import ParserAgent
from backend.agents.router import RouterAgent
from backend.agents.solver import SolverAgent
from backend.agents.verifier import VerifierAgent
from backend.agents.explainer import ExplainerAgent
from backend.schemas import ParsedProblem, RouteDecision, Solution, Verification, Explanation
from backend.memory import SolutionState

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
    
    def __init__(self, parser=None, router=None, solver=None, verifier=None, explainer=None, max_retries=3):
        """
        Initialize Orchestrator with dependency injection support.

        Agents (5 total):
            parser:   Extracts structured problem from raw input
            router:   Classifies domain and strategy
            solver:   Generates SymPy code (Program-of-Thoughts)
            verifier: Validates solution via numerical substitution + LLM judge
            explainer: Produces JEE-specific step-by-step explanation (5th Agent)
        """
        # Dependency Injection with sensible defaults
        self.parser = parser or ParserAgent()
        self.router = router or RouterAgent()
        self.solver = solver or SolverAgent()
        self.verifier = verifier or VerifierAgent()
        self.explainer = explainer or ExplainerAgent()
        self.max_retries = max_retries
        
    def run(self, user_input) -> Dict[str, Any]:
        """
        Run the full SOTA math solving pipeline.
        
        Args:
            user_input: The math problem (text as string OR dictionary with 'latex' and 'problem_data').
            
        Returns:
            Dict containing final response, events, and debug info.
        """
        # Extract displayably text if input is a dict
        display_input = user_input.get("latex", "") if isinstance(user_input, dict) else str(user_input)
        
        # 0. Check for Follow-up / Conversational Intent
        # We leverage the Solver's memory to detect context
        self.solver.memory.add_user_message(display_input)
        follow_up_result = self.parser.is_follow_up(display_input, self.solver.memory.get_context_window(3))
        
        if follow_up_result.get("is_follow_up", False):
            reason = follow_up_result.get("reason", "Detected follow-up question")
            response = self.solver._generate_follow_up_response(display_input)
            events = [reason, "Generated conversational response"]
            self.solver.memory.add_assistant_message(response, events=events)
            return {
                "response": response,
                "events": events,
                "context": None
            }

        # Be sure to set this as the active problem for context
        self.solver.memory.set_active_problem(display_input)

        # Auto-Title Generation
        # We check if title is missing (new session) and this is the first turn
        if not self.solver.memory.session_id:
             # Should practically never happen if memory initialized
             pass
        
        # We really want to check if the session already has a title
        # For now, we launch a fire-and-forget generation if it's the first message
        # But to be safe and simple, we can do it inline for now or just skip if we don't have async background tasks easily set up.
        # Let's do a simple check: if we are in a new session (len messages == 0 before this), generate title.
        
        # ACTUALLY: The memory ALREADY has the user message added a few lines above.
        # So len(messages) would be 1 (User).
        if len(self.solver.memory.messages) == 1:
            try:
                # Generate a short title
                title_prompt = f"Generate a short, descriptive title (3-5 words) for a math session starting with: '{display_input}'. Return ONLY the title, no quotes."
                title = self.solver.client.models.generate_content(
                    model=self.solver.model_name,
                    contents=title_prompt
                ).text.strip().replace('"', '')
                
                self.solver.memory.update_title(title)
            except Exception as e:
                print(f"Title generation failed: {e}")

        ctx = PipelineContext(raw_input=display_input)
        events = []  # Log of what happened (for UI)
        
        # 0. GUARDRAIL: Check if input is math-related
        guard_result = self.parser.is_math_related(display_input)
        if not guard_result.get("is_math", True):
            events.append(f"🚫 Guardrail: {guard_result.get('reason', 'Not math-related')}")
            return {
                "response": "I'm a **Math Mentor** specialized in solving mathematical problems. I can help you with:\n\n- Algebra, Calculus, Geometry\n- Probability & Statistics\n- Proofs and Theorems\n- Mathematical Concepts\n\n**Please ask a math-related question!** 📐",
                "events": events,
                "status": "guardrail_rejected"
            }
        events.append("✅ Guardrail passed: Math-related query")
        
        # 1. Parse
        events.append("Parsing problem...")
        parsed_dict = self.parser.parse(user_input)
        
        # Convert Dict to ParsedProblem Object
        ctx.parsed = ParsedProblem(
            problem_text=parsed_dict.get("problem_statement", ""),
            topic=parsed_dict.get("domain", "unknown"),
            question=parsed_dict.get("question", ""),
            approach=parsed_dict.get("approach", ""),
            features=parsed_dict.get("features", []),
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
                last_error = ctx.attempts[-1].verification.issues[0] if ctx.attempts[-1].verification.issues else ""
                error_hint = self._get_error_hint(last_error)
                
                problem_for_solver += f"\n\n### [PREVIOUS ATTEMPTS FAILED]\n{history}\n"
                if error_hint:
                    problem_for_solver += f"\n**HINT**: {error_hint}\n"
                problem_for_solver += "\n**ACTION**: Review the failures above and generate NEW, corrected code. Avoid repeating the same mistakes."
            
            solution = self.solver.solve(problem_for_solver, features=ctx.parsed.features)
            
            # Record solving mode and RAG context if it's the first attempt
            if i == 0:
                # Show solving mode in events
                solving_mode = solution.get('solving_mode', 'Unknown')
                events.append(f"🧠 Solving Mode: {solving_mode}")
                
                if solution.get('rag_context'):
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
        
        last = ctx.attempts[-1] if ctx.attempts else None

        # 5. Determine the best available solution state
        target_solution = ctx.final_solution if ctx.status == "verified" else (last.solution if last else None)
        target_answer = target_solution.get("answer", "") if target_solution else ""
        target_code = target_solution.get("code", "") if target_solution else ""
        target_reasoning = target_solution.get("reasoning", "") if target_solution else ""
        
        # Guardrail: Is the answer a total failure?
        is_total_failure = target_answer in ["", "Generation Failed", "Error"] or target_solution is None
        
        # D. Explain (5th Agent — JEE Tutor)
        # Only try to explain if we actually produced a mathematically plausible answer
        if not is_total_failure:
            events.append("🎓 Generating JEE Tutor Explanation...")
            try:
                ctx.explanation = self.explainer.explain(
                    problem=ctx.parsed.problem_text,
                    answer=str(target_answer),
                    domain=ctx.parsed.topic,
                    approach=ctx.parsed.approach,
                    rag_context=ctx.rag_context,
                    code=target_code,
                )
                if not ctx.explanation.error:
                    events.append(f"🎓 JEE Tutor Explanation generated (ExplainerAgent) — Chapter: {ctx.explanation.chapter_tag} [{ctx.explanation.difficulty}]")
                else:
                    events.append(f"⚠️ Explainer partial: {ctx.explanation.error}")
            except Exception as _e:
                ctx.explanation = Explanation(error=str(_e))
                events.append(f"⚠️ Explainer failed: {_e}")
        else:
            ctx.explanation = None
            events.append("⏭️ Skipped Explanation generation due to solver failure.")

        # 6. Final Message UI Generation
        msg = ""
        
        # State A: Verification Assistance Needed (Solver ran, answer output, but Verifier is unsure)
        if ctx.status != "verified" and last and getattr(last.verification, 'needs_hitl', False) and not is_total_failure:
            ctx.status = "verification_hitl"
            reasoning = strip_code_from_reasoning(target_reasoning)
            msg = f"### Verification Assistance Needed ⚠️\n\nI've produced an answer, but I am not completely sure if it is correct.\n\n{reasoning}\n\n**Calculated Answer:** {target_answer}\n\n*Why I need help:* {', '.join(last.verification.issues)}\n\nPlease review and let me know if it's correct!"
        
        # State B: Fully Verified
        elif ctx.status == "verified":
            reasoning = strip_code_from_reasoning(target_reasoning)
            msg = f"### Solution\n\n{reasoning}\n\n**Answer:** {target_answer}\n\n"
            if len(ctx.attempts) > 1:
                msg += f"*Verified in {len(ctx.attempts)} attempts (Reflexion Active).*"
                
        # State C: Total Failure or Unverified
        else:
            msg = f"### Solution (Unverified) ⚠️\n\nI struggled to mathematically verify this answer, so **please check it carefully and tell me if it is correct using the ✅ or ❌ buttons below!**\n\n"
            reasoning = strip_code_from_reasoning(target_reasoning)
            if not reasoning:
                reasoning = 'No reasoning available'
            
            msg += f"**My best attempt at reasoning:**\n{reasoning}\n\n**Possible Answer:** {target_answer}\n"
            if last and last.verification.issues:
                msg += f"\n*Issues found trying to verify:* {last.verification.issues}"
        
        # Generator Visual Deck
        # ONLY generate visuals if we have a plausible reasoning chain
        deck = None
        if target_solution and not is_total_failure:
            try:
                events.append("Generating visual explanation...")
                deck = self.solver.solve_structured(
                    ctx.parsed.problem_text, 
                    context={"approach": target_reasoning or "Mathematical solution"}
                )
            except Exception as e:
                events.append(f"Visual generation failed: {e}")
        
        # Build SolutionState from PipelineContext (structured storage)
        last_attempt = ctx.attempts[-1] if ctx.attempts else None
        
        # Calculate confidence first (needed for SolutionState)
        final_confidence = 0.0
        if last_attempt and last_attempt.verification:
            final_confidence = last_attempt.verification.confidence
        
        solution_state = SolutionState(
            rag_context=ctx.rag_context if ctx.rag_context else None,
            solving_mode=events[3] if len(events) > 3 and "Solving Mode" in events[3] else None,  # Extract from events
            code=ctx.final_solution.get('code') if ctx.final_solution else (last_attempt.solution.get('code') if last_attempt else None),
            reasoning=ctx.final_solution.get('reasoning') if ctx.final_solution else (last_attempt.solution.get('reasoning') if last_attempt else None),
            answer=str(ctx.final_solution.get('answer')) if ctx.final_solution else (str(last_attempt.solution.get('answer')) if last_attempt else None),
            is_verified=(ctx.status == "verified"),
            confidence=final_confidence,
            verification_issues=last_attempt.verification.issues if last_attempt and last_attempt.verification else [],
            reflexion_attempts=len(ctx.attempts)
        )
        
        # Save solution to memory WITH deck AND solution_state and events
        self.solver.memory.add_assistant_message(msg, deck, solution_state, events)

        return {
            "response": msg,
            "events": events,
            "context": ctx,
            "deck": deck,
            "confidence": final_confidence,
            "solution_state": solution_state
        }

    def _format_history(self, attempts: List[Attempt]) -> str:
        """Format detailed reflexion history for the LLM solver to learn from."""
        if not attempts:
            return ""
        
        history_parts = []
        for att in attempts:
            part = f"--- ATTEMPT {att.round + 1} ---\n"
            part += f"CODE USED:\n```python\n{att.solution.get('code', '')}\n```\n"
            if att.solution.get('answer'):
                part += f"RESULT: {att.solution['answer']}\n"
            if att.verification.issues:
                part += f"ISSUES: {', '.join(att.verification.issues)}\n"
            if att.reflection:
                part += f"REFLECTION: {att.reflection}\n"
            history_parts.append(part)
        
        return "\n".join(history_parts)

    def _get_error_hint(self, error_msg: str) -> str:
        """Map common technical errors to helpful SymPy hints."""
        error_msg = str(error_msg).lower()
        
        if "'int' object has no attribute 'subs'" in error_msg:
            return "You are mixing Python integers with SymPy symbols. Ensure you are using SymPy's 'Piecewise', 'Integer', or 'S()' if you need to call '.subs()' on a value. Keep expressions symbolic as long as possible."
        
        if "can't multiply sequence by non-int of type" in error_msg or "list indices must be integers" in error_msg:
            return "SymPy 'solve' often returns a list. Access the solution element (e.g., sol[0]) before using it in calculations."
            
        if "name 'x' is not defined" in error_msg:
            return "Ensure all variables are defined as symbols: x = symbols('x')"
            
        if "timed out" in error_msg:
            return "The solution is too complex for symbolic integration. Try using 'nsolve' for a numerical approximation or simplify the problem before solving."

        return ""
    
    # Facade methods for cleaner frontend access
    def add_user_message(self, content: str):
        """Facade: Add user message to conversation memory."""
        self.solver.memory.add_user_message(content)
    
    def add_assistant_message(self, content: str, deck=None, solution_state=None, events=None):
        """Facade: Add assistant message to conversation memory."""
        self.solver.memory.add_assistant_message(content, deck, solution_state, events)
    
    def restore_session(self) -> bool:
        """Facade: Restore last conversation session."""
        return self.solver.memory.restore_last_session()
    
    def clear_conversation(self):
        """Facade: Clear conversation history."""
        self.solver.memory.clear()
    
    def get_conversation_context(self, limit: int = 5) -> str:
        """Facade: Get recent conversation context."""
        return self.solver.memory.get_context_window(limit)
