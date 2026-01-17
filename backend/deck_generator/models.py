"""
Pydantic Models for Math Deck Generation.
Defines the strict schema for LLM structured output.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class VisualRequest(BaseModel):
    """Request for a specific visualization."""
    # Removed ConfigDict - Gemini doesn't support 'additionalProperties'
    
    type: Literal["parabola", "triangle", "number_line", "coordinate_plane", "unit_circle", "generic"] = Field(
        ..., 
        description="The type of diagram to generate."
    )
    # Use specific optional fields instead of Dict[str, Any]
    a: Optional[float] = Field(None, description="Coefficient a (for parabola y=ax^2+bx+c)")
    b: Optional[float] = Field(None, description="Coefficient b")
    c: Optional[float] = Field(None, description="Coefficient c")
    caption: Optional[str] = Field(None, description="Caption to display below the diagram")


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


