"""
Explainer/Tutor Agent — JEE-aware solution explainer (5th Agent).

Responsibilities:
- Takes a VERIFIED answer from the Verifier and produces a structured,
  JEE Mains/Advanced-specific explanation.
- Does NOT solve or verify — purely educational output.
- Persona: IIT Coaching Faculty with 15+ years experience.
"""

import json
import re
from typing import Optional

from backend.agents.base import BaseAgent
from backend.schemas import Explanation


class ExplainerAgent(BaseAgent):
    """
    The JEE Tutor — produces student-friendly, exam-ready explanations.

    Input:  Verified answer + problem context
    Output: Structured Explanation with JEE chapter tag, difficulty,
            step-by-step breakdown, exam shortcut, tips, and common mistakes.

    This is the 5th agent in the pipeline:
    Parser → Router → Solver → Verifier → Explainer
    """

    def explain(
        self,
        problem: str,
        answer: str,
        domain: str = "",
        approach: str = "",
        rag_context: str = "",
        code: str = "",
    ) -> Explanation:
        """
        Generate a JEE-specific explanation for a solved problem.

        Args:
            problem:     Original problem text (from ParsedProblem.problem_text)
            answer:      Verified answer string (from Executor output)
            domain:      Problem domain, e.g. "probability", "calculus"
            approach:    Suggested approach from Parser
            rag_context: Retrieved KB chunks (from Solver's RAG retrieval)
            code:        SymPy code that produced the answer (for reference)

        Returns:
            Explanation dataclass with JEE-specific fields populated.
            On any failure, returns Explanation(error=<message>).
        """
        prompt = self._build_prompt(problem, answer, domain, approach, rag_context, code)

        try:
            raw_response = self._call_llm(prompt)
            return self._parse_response(raw_response)
        except Exception as e:
            self._log(f"ExplainerAgent failed: {e}", level="error")
            return Explanation(error=str(e))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_prompt(
        self,
        problem: str,
        answer: str,
        domain: str,
        approach: str,
        rag_context: str,
        code: str,
    ) -> str:
        """Load and fill the JEE explainer prompt template."""
        try:
            from backend.prompts import get_prompt
            template = get_prompt("explainer_prompt")
        except Exception:
            # Hard fallback if prompt loader fails
            template = self._fallback_prompt_template()

        # Sanitise optional fields so {placeholder} errors don't crash render
        return template.format(
            problem=problem,
            answer=answer,
            domain=domain or "mathematics",
            approach=approach or "standard method",
            rag_context=rag_context or "No additional context retrieved.",
            code=code or "# No code available",
        )

    def _parse_response(self, raw: str) -> Explanation:
        """
        Parse Gemini's JSON response into an Explanation object.

        Handles:
        - Markdown code fences (```json ... ```)
        - Partial JSON (graceful degradation)
        - Unexpected field types
        """
        # Strip markdown fences if present
        cleaned = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to extract JSON object with regex as last resort
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    return Explanation(
                        intuition=cleaned,  # Save raw text as intuition
                        error="JSON parse failed — raw text preserved in intuition"
                    )
            else:
                return Explanation(
                    intuition=cleaned,
                    error="Could not extract JSON from response"
                )

        # Build Explanation — be defensive about each field type
        steps = data.get("steps", [])
        if isinstance(steps, list):
            # Normalise: each step must be a dict with step_title + step_content
            normalised_steps = []
            for s in steps:
                if isinstance(s, dict):
                    normalised_steps.append({
                        "step_title": str(s.get("step_title", "")),
                        "step_content": str(s.get("step_content", "")),
                    })
                elif isinstance(s, str):
                    normalised_steps.append({"step_title": "", "step_content": s})
        else:
            normalised_steps = []

        difficulty = str(data.get("difficulty", ""))
        # Enforce allowed values
        if difficulty not in ("Mains", "Advanced", "Both"):
            difficulty = "Mains"  # conservative default

        return Explanation(
            intuition=str(data.get("intuition", "")),
            steps=normalised_steps,
            jee_shortcut=str(data.get("jee_shortcut", "")),
            tips=_ensure_list(data.get("tips", [])),
            common_mistakes=_ensure_list(data.get("common_mistakes", [])),
            difficulty=difficulty,
            chapter_tag=str(data.get("chapter_tag", "")),
            error=None,
        )

    def _fallback_prompt_template(self) -> str:
        """Minimal fallback prompt if the .md file cannot be loaded."""
        return """You are a JEE coaching expert. A student solved this problem:

Problem: {problem}
Answer: {answer}
Domain: {domain}

Explain the solution with JEE exam focus. Output ONLY a JSON object:
{{
  "intuition": "...",
  "steps": [{{"step_title": "...", "step_content": "..."}}],
  "jee_shortcut": "...",
  "tips": ["..."],
  "common_mistakes": ["..."],
  "difficulty": "Mains",
  "chapter_tag": "..."
}}"""


# ------------------------------------------------------------------
# Module-level utility
# ------------------------------------------------------------------

def _ensure_list(value) -> list:
    """Guarantee a list is returned regardless of LLM output type."""
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value] if value else []
    return []


# ------------------------------------------------------------------
# Standalone test
# ------------------------------------------------------------------

if __name__ == "__main__":
    agent = ExplainerAgent()

    result = agent.explain(
        problem="Three students S1, S2, S3 can solve a problem with probabilities 1/3, 1/4, 1/5. Find P(at least one solves).",
        answer="3/5",
        domain="probability",
        approach="complement rule",
        rag_context="",
        code="from sympy import *\nanswer = 1 - Rational(2,3)*Rational(3,4)*Rational(4,5)",
    )

    if result.error:
        print(f"❌ Error: {result.error}")
    else:
        print(f"📚 Chapter: {result.chapter_tag}  [{result.difficulty}]")
        print(f"\n💡 Intuition:\n{result.intuition}")
        print(f"\n⚡ JEE Shortcut:\n{result.jee_shortcut}")
        print(f"\n📋 Steps ({len(result.steps)}):")
        for s in result.steps:
            print(f"  - {s['step_title']}")
        print(f"\n✅ Tips:")
        for t in result.tips:
            print(f"  • {t}")
        print(f"\n⚠️  Common Mistakes:")
        for m in result.common_mistakes:
            print(f"  ✗ {m}")
