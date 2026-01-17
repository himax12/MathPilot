import sys
import os
import unittest
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.deck_generator.models import MathDeck, MathSlide, VisualRequest
    from backend.deck_generator.generator import DeckGenerator
    from backend.agents.solver import SolverAgent
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)

class TestPhase3(unittest.TestCase):
    def test_models(self):
        """Verify Pydantic models structure."""
        deck = MathDeck(
            title="Test Deck",
            slides=[
                MathSlide(
                    type="title",
                    title="Welcome",
                    content="Hello"
                )
            ],
            final_answer="42"
        )
        self.assertEqual(deck.final_answer, "42")
        print("✅ Models verified")

    def test_generator(self):
        """Verify separate Generator pipeline."""
        deck = MathDeck(
            title="Pythagoras",
            slides=[
                MathSlide(type="title", title="Intro", content="# Hi"),
                MathSlide(
                    type="visualization", 
                    title="See Triangle", 
                    content="Look at this",
                    visual_request=VisualRequest(
                        type="triangle",
                        params={"vertices": [(0,0), (3,0), (0,4)]}
                    )
                )
            ],
            final_answer="5"
        )
        
        gen = DeckGenerator(theme="dark")
        html = gen.from_structured(deck)
        
        self.assertIn("Pythagoras", html)
        self.assertIn("data:image/png;base64", html) # Check if image generated
        print("✅ Generator pipeline verified")

if __name__ == '__main__':
    unittest.main()
