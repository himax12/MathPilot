"""
Test Script for Deck Generator
Run this to validate the module works correctly.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from deck_generator import DeckGenerator


def test_structured_input():
    """Test with structured input data."""
    print("=" * 60)
    print("TEST 1: Structured Input")
    print("=" * 60)
    
    deck = DeckGenerator(theme="dark")
    
    html = deck.generate(
        title="Solving Quadratic Equations",
        intuition="A quadratic equation can be solved using the quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$",
        steps=[
            {"number": 1, "content": "Identify the coefficients:\n- $a = 1$\n- $b = 3$\n- $c = -4$"},
            {"number": 2, "content": "Calculate the discriminant:\n- $\\Delta = b^2 - 4ac = 9 + 16 = 25$"},
            {"number": 3, "content": "Apply the formula:\n- $x = \\frac{-3 \\pm 5}{2}$\n- $x_1 = 1$, $x_2 = -4$"},
        ],
        answer="x = 1 or x = -4",
        domain="algebra"
    )
    
    # Save and preview
    output_path = os.path.join(os.path.dirname(__file__), "test_output_structured.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated: {output_path}")
    print(f"   File size: {len(html)} bytes")
    return output_path


def test_reasoning_text_parsing():
    """Test parsing from raw reasoning text."""
    print("\n" + "=" * 60)
    print("TEST 2: Reasoning Text Parsing")
    print("=" * 60)
    
    sample_reasoning = """
**INTUITION**:
This is a probability problem. We need to find P(at least one succeeds) using the complement rule.

**SOLUTION STEPS**:

**Step 1**: Identify probabilities
- P(S1) = 1/3
- P(S2) = 1/10
- P(S3) = 1/12

**Step 2**: Calculate P(none succeed)
- P(fail S1) = 2/3
- P(fail S2) = 9/10
- P(fail S3) = 11/12
- P(none) = (2/3) × (9/10) × (11/12) = 198/360 = 11/20

**Step 3**: Apply complement rule
- P(at least one) = 1 - P(none) = 1 - 11/20 = **9/20**

**EXPLANATION**:
The probability that at least one student solves the problem is 9/20 or 45%.
"""
    
    deck = DeckGenerator(theme="dark")
    html = deck.from_reasoning_text(
        raw_text=sample_reasoning,
        answer="9/20 = 0.45 = 45%",
        title="Probability: At Least One Success"
    )
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "test_output_parsed.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated: {output_path}")
    print(f"   File size: {len(html)} bytes")
    return output_path


def test_with_diagram():
    """Test with auto-generated diagram."""
    print("\n" + "=" * 60)
    print("TEST 3: With Auto-Generated Diagram")
    print("=" * 60)
    
    deck = DeckGenerator(theme="dark")
    
    html = deck.generate(
        title="Triangle Area Calculation",
        intuition="For a right triangle, Area = (1/2) × base × height",
        steps=[
            {"number": 1, "content": "Given: Base = 6 units, Height = 8 units"},
            {"number": 2, "content": "Apply formula: Area = (1/2) × 6 × 8 = 24 square units"},
        ],
        answer="Area = 24 square units",
        domain="geometry"  # This triggers diagram generation
    )
    
    output_path = os.path.join(os.path.dirname(__file__), "test_output_diagram.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated: {output_path}")
    print(f"   File size: {len(html)} bytes")
    return output_path


def main():
    """Run all tests."""
    print("\n🧪 DECK GENERATOR MODULE TEST\n")
    
    try:
        path1 = test_structured_input()
        path2 = test_reasoning_text_parsing()
        path3 = test_with_diagram()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nGenerated files:")
        print(f"  1. {path1}")
        print(f"  2. {path2}")
        print(f"  3. {path3}")
        print("\nOpen any of these in a browser to see the result!")
        
        # Optionally open the first one
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(path1)}')
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
