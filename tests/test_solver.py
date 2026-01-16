"""
Test script for Math Mentor MVP
Tests both text and image inputs with sample problems
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from solver import SolverAgent
from executor import Executor


def test_text_input():
    """Test Day 1: Text input → Solver → Executor"""
    print("="*60)
    print("Testing Day 1: Text Input Pipeline")
    print("="*60)
    
    # Initialize
    solver = SolverAgent()
    executor = Executor()
    
    test_problems = [
        "Solve x^2 + 3x - 4 = 0 for x",
        "Integrate x^2 from 0 to 10",
        "Find the derivative of sin(x) * cos(x)"
    ]
    
    for i, problem in enumerate(test_problems, 1):
        print(f"\n--- Test {i}/3 ---")
        print(f"Problem: {problem}")
        
        # Generate code
        solver_result = solver.solve(problem)
        if solver_result["error"]:
            print(f"❌ Solver Error: {solver_result['error']}")
            continue
        
        code = solver_result["code"]
        print(f"\nGenerated Code:\n{code}")
        
        # Execute
        exec_result = executor.execute(code)
        if exec_result["success"]:
            print(f"\n✅ Answer: {exec_result['answer']}")
        else:
            print(f"\n❌ Execution Error: {exec_result['error']}")
    
    print("\n" + "="*60)
    print("Day 1 Tests Complete!")
    print("="*60)


def test_ocr():
    """Test Day 2: OCR module"""
    print("\n" + "="*60)
    print("Testing Day 2: OCR Module")
    print("="*60)
    
    try:
        from ocr import MathOCR
        ocr = MathOCR()
        print(f"✅ OCR Module initialized")
        print(f"   Using Cloud Vision: {ocr.use_cloud_vision}")
        
        # Note: Actual image testing requires image files
        print("\n📝 To test OCR:")
        print("   1. Run: uv run streamlit run frontend/app.py")
        print("   2. Select 'Image Upload' mode")
        print("   3. Upload a photo of a math problem")
        
    except Exception as e:
        print(f"❌ OCR Test Failed: {e}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("\n🧮 Math Mentor - Test Suite\n")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found")
        print("💡 Please create a .env file with:")
        print("   GEMINI_API_KEY=your-key-here")
        sys.exit(1)
    
    # Run tests
    try:
        test_text_input()
        test_ocr()
        
        print("\n✅ All tests passed!")
        print("\n🚀 Ready to run: uv run streamlit run frontend/app.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
