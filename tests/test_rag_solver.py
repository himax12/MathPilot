"""
Test script for RAG-enabled Solver Agent.
"""

from backend.agents.solver import SolverAgent

def test_rag():
    print("Initializing Solver with RAG...")
    try:
        solver = SolverAgent()
    except Exception as e:
        print(f"Failed to init solver: {e}")
        return

    if getattr(solver, 'rag', None) and solver.rag.ready:
        print("✅ RAG is ready")
        
        # Test retrieval
        query = "integration by parts"
        print(f"\nRetrieving context for: '{query}'")
        context = solver.rag.retrieve(query, top_k=1)
        
        if context:
            print(f"✅ Context retrieved ({len(context)} chars)")
            print("Preview:")
            print("-" * 20)
            print(context[:200] + "...")
            print("-" * 20)
        else:
            print("⚠️ No context retrieved (Result empty)")

        # Test Solve
        problem = "Integrate x * e^x from 0 to 1"
        print(f"\nSolving: '{problem}'")
        result = solver.solve(problem)
        
        if result['error']:
            print(f"❌ Solve Error: {result['error']}")
        else:
            print("✅ Code generated successfully")
            print(result['code'][:100] + "...")
            
    else:
        print("⚠️ RAG not ready (Index missing or dependencies failed)")
        print("Please ensure 'backend/knowledge/index/jee_math.index' exists.")

if __name__ == "__main__":
    test_rag()
