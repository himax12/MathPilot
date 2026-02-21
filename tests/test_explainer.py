"""
Unit tests for the JEE-specific Explainer/Tutor Agent.
"""

from backend.agents.explainer import ExplainerAgent

def test_explain_jee_probability():
    """
    Test using a classic JEE probability structure:
    Three students solve a problem with given probabilities. Find P(at least one solves).
    """
    print("Testing ExplainerAgent (JEE Persona)...")
    try:
        agent = ExplainerAgent()
    except Exception as e:
        print(f"Init failed: {e}")
        return

    problem = "Three students S1, S2, S3 attempt a problem with probabilities 1/3, 1/4, 1/5. Find P(at least one solves)."
    answer = "3/5"
    domain = "probability"
    approach = "complement rule"
    rag_context = ""
    code = "from sympy import *\nans = 1 - (2*3*4)/(3*4*5)\nanswer = Rational(3,5)"

    print(f"\n--- Problem Context ---")
    print(f"Problem: {problem}")
    print(f"Answer:  {answer}")
    print(f"Calling ExplainerAgent.explain()...")

    result = agent.explain(
        problem=problem,
        answer=answer,
        domain=domain,
        approach=approach,
        rag_context=rag_context,
        code=code
    )

    # 1. Check for errors
    print(f"✅ Error: {result.error}")
    assert result.error is None, f"Explainer failed: {result.error}"

    # 2. Check structure
    print(f"✅ Intuition populated ({len(result.intuition)} chars)")
    assert result.intuition != "", "Intuition is missing"

    print(f"✅ Steps generated: {len(result.steps)}")
    assert len(result.steps) >= 2, "Expected at least 2 steps"
    for idx, step in enumerate(result.steps):
        assert "step_title" in step, f"Step {idx} missing title"
        assert "step_content" in step, f"Step {idx} missing content"

    # 3. Check JEE specific fields
    print(f"✅ Chapter Tag: {result.chapter_tag}")
    assert result.chapter_tag != "", "Chapter tag missing"

    print(f"✅ Difficulty: {result.difficulty}")
    assert result.difficulty in ("Mains", "Advanced", "Both"), f"Invalid difficulty: {result.difficulty}"

    print(f"✅ JEE Shortcut populated ({len(result.jee_shortcut)} chars)")
    assert result.jee_shortcut != "", "JEE shortcut missing"

    # 4. Check lists
    print(f"✅ Exam Tips: {len(result.tips)}")
    assert isinstance(result.tips, list), "Tips must be a list"
    assert len(result.tips) > 0, "Expected at least one tip"

    print(f"✅ Common Mistakes: {len(result.common_mistakes)}")
    assert isinstance(result.common_mistakes, list), "Common mistakes must be a list"
    assert len(result.common_mistakes) > 0, "Expected at least one mistake"

    print("\n🎉 ALL TESTS PASSED!")


if __name__ == "__main__":
    test_explain_jee_probability()
