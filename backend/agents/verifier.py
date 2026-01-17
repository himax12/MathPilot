"""
Verifier Agent - Validates solutions using multi-method verification.
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
from schemas import Verification
from config import config
from executor import Executor

class VerifierAgent(BaseAgent):
    """
    The Quality Assurance Engineer.
    
    Responsibilities:
    1. Numerical Substitution: Plug answer back into problem.
    2. Constraint Validation: Check if answer satisfies domain (e.g., x > 0).
    3. Common Sense Check: Is the magnitude/unit realistic?
    """
    
    def __init__(self, model_name: str = None):
        super().__init__(model_name)
        self.executor = Executor(timeout_seconds=5)
        
    def verify(self, problem_text: str, original_code: str, answer: str) -> Verification:
        """
        Run verification suite on the solution.
        
        Args:
            problem_text: The original problem.
            original_code: The PoT code that generated the answer.
            answer: The answer string (e.g. "[-2, 2]").
            
        Returns:
            Verification object.
        """
        checks = []
        issues = []
        
        # Check 1: LLM-driven Sanity Code Generation
        # We ask the LLM to write code that verifies the answer
        try:
            verify_code = self._generate_verification_code(problem_text, answer)
            if verify_code:
                result = self.executor.execute(verify_code)
                
                check_info = {
                    "type": "numerical_substitution",
                    "code": verify_code,
                    "passed": False,
                    "details": ""
                }
                
                if result["success"]:
                    # Expecting True or a list of Trues
                    res_val = result["answer"]
                    is_valid = str(res_val).lower() == "true" or (isinstance(res_val, list) and all(str(r).lower() == "true" for r in res_val))
                    
                    check_info["passed"] = is_valid
                    check_info["details"] = f"Result: {res_val}"
                    if not is_valid:
                        issues.append(f"Numerical substitution failed: {res_val}")
                else:
                    check_info["details"] = f"Execution Error: {result['error']}"
                    issues.append(f"Verification code failed to run: {result['error']}")
                
                checks.append(check_info)
        except Exception as e:
            self._log(f"Verification Check 1 failed: {e}")

        # Check 2: Conceptual Sanity Check (LLM Judge)
        try:
            sanity_prompt = self._build_sanity_prompt(problem_text, answer)
            sanity_resp = self._call_llm(sanity_prompt)
            
            # Simple keyword parsing (Robust enough for now)
            passed_sanity = "VALID" in sanity_resp.upper()
            explanation = sanity_resp.replace("VALID", "").replace("INVALID", "").strip()
            
            checks.append({
                "type": "conceptual_sanity",
                "passed": passed_sanity,
                "details": explanation
            })
            
            if not passed_sanity:
                issues.append(f"Conceptual check failed: {explanation}")
                
        except Exception as e:
            self._log(f"Verification Check 2 failed: {e}")

        # Aggregate Results
        # If any major check fails, we flag it
        is_valid = len(issues) == 0
        confidence = 1.0 if is_valid else 0.4
        
        return Verification(
            is_valid=is_valid,
            confidence=confidence,
            issues=issues,
            checks_performed=checks,
            needs_hitl=not is_valid
        )

    def _generate_verification_code(self, problem: str, answer: str) -> Optional[str]:
        """Generate SymPy code to substitute answer back."""
        prompt = f"""
Write Python SymPy code to verify if the answer `{answer}` is correct for the problem: "{problem}".

Rules:
1. Define the variables and equation from the problem.
2. Substitute the answer into the equation.
3. Check if LHS - RHS == 0 (or close to 0).
4. Store the result boolean (True/False) in variable `answer`.
5. Output ONLY code inside ```python``` tags.
"""
        response = self._call_llm(prompt)
        # Reuse solver's extraction logic if I had access, but simple regex works
        match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
        if match:
             return match.group(1).strip()
        return response.strip()

    def _build_sanity_prompt(self, problem: str, answer: str) -> str:
        return f"""
You are a Math Judge.
Problem: "{problem}"
Proposed Answer: "{answer}"

Is this answer reasonable?
- Check units (time cannot be negative).
- Check domain (log of negative).
- Check magnitude.

Output EXACTLY one line:
"VALID" if it makes sense.
"INVALID: <reason>" if it does not.
"""
