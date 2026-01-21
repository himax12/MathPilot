"""
Test script for Router Agent.
Verifies that the router correctly classifies different types of math problems.
"""

from backend.agents.router import RouterAgent
from backend.config import config

def test_router():
    print("Testing Router Agent...")
    
    if not config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not set. Skipping test.")
        return

    router = RouterAgent()
    
    test_cases = [
        # Algebra
        "Solve x^2 + 5x + 6 = 0",
        # Calculus
        "Find the derivative of sin(x) * x^2",
        # Probability
        "If P(A) = 0.5 and P(B|A) = 0.2, find P(A and B)",
        # Ambiguous / General
        "What is 2 + 2?"
    ]
    
    for problem in test_cases:
        print(f"\nProblem: {problem}")
        decision = router.route(problem)
        print(f"Domain: {decision.domain}")
        print(f"Subtopic: {decision.subtopic}")
        print(f"Strategy: {decision.strategy}")
        print(f"RAG Filters: {decision.rag_filters}")
        print(f"Confidence: {decision.confidence}")
        
        # Basic assertion logic
        if "x^2" in problem and decision.domain.lower() not in ["algebra", "general"]:
            print("⚠️ Unexpected domain for algebra problem")
        elif "derivative" in problem and decision.domain.lower() != "calculus":
             print("⚠️ Unexpected domain for calculus problem")

if __name__ == "__main__":
    test_router()
