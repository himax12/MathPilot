"""
Pydantic Models for Math Deck Generation.
Defines the strict schema for LLM structured output.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Point2D(BaseModel):
    """A 2D coordinate point."""
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    label: Optional[str] = Field(None, description="Optional text label for this point")

class GeometricElement(BaseModel):
    """A geometric primitive to be rendered on an axis."""
    type: Literal["point", "line", "polygon", "circle", "angle"] = Field(
        ...,
        description="The type of geometric primitive."
    )
    points: List[Point2D] = Field(
        ...,
        description="Coordinates defining the element. 1 for point/circle, 2 for line, 3+ for polygon/angle."
    )
    radius: Optional[float] = Field(None, description="Radius for circle type")
    label: Optional[str] = Field(None, description="Optional label for the element (e.g., side length, angle measure)")

class VisualRequest(BaseModel):
    """Request for a specific visualization."""
    # Removed ConfigDict - Gemini doesn't support 'additionalProperties'
    
    type: Literal["geometry", "parabola", "triangle", "number_line", "coordinate_plane", "unit_circle", "generic"] = Field(
        ..., 
        description="The type of diagram to generate. Use 'geometry' for custom geometric constructions."
    )
    
    # Specific optional fields for backwards compatibility or specialized types
    a: Optional[float] = Field(None, description="Coefficient a (for parabola y=ax^2+bx+c)")
    b: Optional[float] = Field(None, description="Coefficient b")
    c: Optional[float] = Field(None, description="Coefficient c")
    caption: Optional[str] = Field(None, description="Caption to display below the diagram")
    
    # New geometric primitives field
    elements: Optional[List[GeometricElement]] = Field(
        None, 
        description="List of geometric primitives to draw. Provide points with their precise coordinates."
    )


class MathSlide(BaseModel):
    """A single slide content."""
    # Removed ConfigDict - Gemini doesn't support 'additionalProperties'
    
    type: Literal["title", "intuition", "step", "visualization", "answer"] = Field(
        ...,
        description="The role of this slide."
    )
    title: str = Field(..., description="The main heading for the slide")
    content: str = Field(..., description="The main text content (Markdown supported).")
    
    # Optional fields
    step_number: Optional[int] = Field(None, description="If type is 'step', the sequence number.")
    visual_request: Optional[VisualRequest] = Field(
        None, 
        description="Dynamic request for a diagram to be rendered on this slide."
    )
    speaker_notes: Optional[str] = Field(None, description="Text for TTS narration.")


class MathDeck(BaseModel):
    """The structure of the complete explanation deck."""
    # Removed ConfigDict - Gemini doesn't support 'additionalProperties'
    
    title: str = Field(..., description="Title of the problem/solution")
    slides: List[MathSlide] = Field(..., description="Ordered list of slides")
    final_answer: str = Field(..., description="The final computed answer (concise)")


