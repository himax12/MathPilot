import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.deck_generator.models import MathDeck, MathSlide, VisualRequest, GeometricElement, Point2D
from backend.deck_generator.generator import DeckGenerator

def test():
    print("Creating deck object...")
    deck = MathDeck(
        title="Test Geometry Deck",
        slides=[
            MathSlide(
                type="title",
                title="Geometry Test",
                content="Testing geometric primitives"
            ),
            MathSlide(
                type="visualization",
                title="Triangle with altitude and incircle",
                content="Look at this beautiful holistic geometry",
                visual_request=VisualRequest(
                    type="geometry",
                    elements=[
                        GeometricElement(
                            type="polygon",
                            points=[Point2D(x=0,y=0,label="A"), Point2D(x=6,y=0,label="B"), Point2D(x=3,y=4,label="C")]
                        ),
                        GeometricElement(
                            type="line",
                            points=[Point2D(x=3,y=4), Point2D(x=3,y=0,label="D")],
                            label="Altitude"
                        ),
                        GeometricElement(
                            type="circle",
                            points=[Point2D(x=3,y=1.5,label="I")],
                            radius=1.5
                        )
                    ]
                )
            )
        ],
        final_answer="A holistic success"
    )

    print("Generating HTML...")
    gen = DeckGenerator(theme="dark")
    html = gen.from_structured(deck)
    
    print("Saving test output...")
    with open(os.path.join(os.path.dirname(__file__), "test_output_holistic.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Done! Open backend/deck_generator/test_output_holistic.html to view.")

if __name__ == "__main__":
    test()
