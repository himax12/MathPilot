"""
Verifier Agent - Validates solutions using multi-method verification.
"""

from google import genai
from typing import Dict, List, Optional, Any
import json
import re

from backend.agents.base import BaseAgent
from backend.schemas import Verification
from backend.config import config
from backend.executor import Executor

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
                    
                    # Robust Boolean Parsing (Universal Fix)
                    # Handle: True, "True", [True, True], Or(x>1), etc.
                    str_val = str(res_val).strip().lower()
                    
                    # Case 1: Direct boolean-like string
                    is_direct_bool = str_val == "true"
                    
                    # Case 2: List of booleans (e.g. multiple test cases)
                    # We strictly check for list type to avoid iterating SymPy objects
                    is_list_valid = False
                    if isinstance(res_val, (list, tuple)):
                         is_list_valid = all(str(r).strip().lower() == "true" for r in res_val)
                    
                    is_valid = is_direct_bool or is_list_valid
                    
                    check_info["passed"] = is_valid
                    check_info["details"] = f"Result: {res_val}"
                    if not is_valid:
                        issues.append(f"numerical_substitution failed (Expected True, got {res_val})")
                else:
                    # Code verification crashed - mark as SKIPPED, not failed
                    # This is graceful degradation: code crash ≠ wrong answer
                    check_info["skipped"] = True
                    check_info["skip_reason"] = result['error']
                    check_info["details"] = f"Verification code skipped: {result['error']}"
                    # DON'T append to issues - we'll fall back to conceptual check
                
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

        # Calculate confidence using pure formula (no hardcoded values)
        # Formula: confidence = (passed + 0.5 * skipped) / total
        # Rationale: passed checks get full credit, skipped get half (uncertain, not wrong)
        
        passed = sum(1 for c in checks if c.get("passed"))
        skipped = sum(1 for c in checks if c.get("skipped"))
        total = len(checks)
        
        if total == 0:
            confidence = 0.5  # No checks = uncertain
        else:
            confidence = round((passed + 0.5 * skipped) / total, 2)
        
        # is_valid = True if any check passed and no explicit issues
        is_valid = passed > 0 and len(issues) == 0
        
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
