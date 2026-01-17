"""
Test script for Orchestrator (Reflexion Pipeline).
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from orchestrator import Orchestrator

def test_pipeline():
    print("Initializing Orchestrator (Reflexion Architecture)...")
    try:
        orch = Orchestrator()
    except Exception as e:
        print(f"Init Error: {e}")
        return
    
    problem = "Find the roots of x^2 - 16 = 0"
    print(f"\nRunning Pipeline for: '{problem}'")
    print("-" * 40)
    
    try:
        result = orch.run(problem)
        
        print("\n--- Execution Trace (Events) ---")
        for event in result['events']:
            print(f"  > {event}")
            
        print("\n--- Final Response ---")
        print(result['response'])
        
        ctx = result.get('context')
        if ctx and ctx.status == 'verified':
            print(f"\n✅ SUCCESS: Pipeline Verified Solution in {len(ctx.attempts)} attempt(s).")
        else:
            print("\n⚠️ PARTIAL: Pipeline Finished Unverified.")
            
    except Exception as e:
        print(f"\n❌ Runtime Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pipeline()
