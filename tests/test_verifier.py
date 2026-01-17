"""
Test script for Verifier Agent.
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents.verifier import VerifierAgent

def test_verifier():
    print("Testing Verifier Agent...")
    try:
        verifier = VerifierAgent()
    except Exception as e:
        print(f"Init failed: {e}")
        return

    # Case 1: Correct Answer
    problem = "Solve x^2 - 4 = 0"
    answer = "[-2, 2]"
    print(f"\n--- Case 1: Correct Answer ---\nProblem: {problem}\nAnswer: {answer}")
    res = verifier.verify(problem, "", answer)
    print(f"✅ Is Valid: {res.is_valid}")
    if not res.is_valid:
        print(f"❌ Issues: {res.issues}")
    
    # Case 2: Incorrect Answer
    problem = "Solve x + 5 = 10"
    answer = "3" 
    print(f"\n--- Case 2: Incorrect Answer ---\nProblem: {problem}\nAnswer: {answer}")
    res = verifier.verify(problem, "", answer)
    print(f"✅ Is Valid: {res.is_valid}")
    if not res.is_valid:
        print(f"❌ Issues: {res.issues}")
    
    # Case 3: Nonsense
    problem = "What is the time taken?"
    answer = "-5 seconds"
    print(f"\n--- Case 3: Sanity Check ---\nProblem: {problem}\nAnswer: {answer}")
    res = verifier.verify(problem, "", answer)
    print(f"✅ Is Valid: {res.is_valid}")
    if not res.is_valid:
        print(f"❌ Issues: {res.issues}")

if __name__ == "__main__":
    test_verifier()
