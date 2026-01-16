"""
OCR Module - Extracts math expressions from images.
Uses Google Cloud Vision + Gemini Vision for robust extraction.
"""

from google import genai
from google.cloud import vision
import os
import base64
from typing import Dict, Optional
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()


class MathOCR:
    """
    Extracts mathematical expressions from images using dual-model approach:
    1. Google Cloud Vision (fast, good for printed text)
    2. Gemini Vision (semantic understanding, repairs OCR errors)
    """
    
    def __init__(self):
        """Initialize OCR clients."""
        # Gemini Vision for semantic LaTeX extraction
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash-exp"
        
        # Google Cloud Vision (optional, falls back to Gemini-only if not configured)
        self.use_cloud_vision = False
        try:
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                self.vision_client = vision.ImageAnnotatorClient()
                self.use_cloud_vision = True
        except Exception:
            pass  # Fall back to Gemini-only mode
    
    def extract_from_image(self, image_bytes: bytes) -> Dict[str, any]:
        """
        Extract math expression from image.
        
        Args:
            image_bytes: Image file as bytes
            
        Returns:
            Dict with:
                - 'latex': Extracted LaTeX string
                - 'confidence': Confidence score (0-1)
                - 'method': Which method was used (cloud_vision, gemini_vision)
                - 'raw_text': Raw OCR output (if available)
                - 'needs_review': Boolean flag for HITL
                - 'error': Error message if extraction failed
        """
        # Try Cloud Vision first if available
        raw_text = None
        if self.use_cloud_vision:
            try:
                raw_text = self._cloud_vision_ocr(image_bytes)
            except Exception as e:
                print(f"Cloud Vision failed: {e}, falling back to Gemini")
        
        # Use Gemini Vision for semantic extraction
        try:
            result = self._gemini_vision_extract(image_bytes, raw_text)
            return result
        except Exception as e:
            return {
                "latex": None,
                "confidence": 0.0,
                "method": "failed",
                "raw_text": raw_text,
                "needs_review": True,
                "error": str(e)
            }
    
    def _cloud_vision_ocr(self, image_bytes: bytes) -> str:
        """Extract raw text using Google Cloud Vision."""
        image = vision.Image(content=image_bytes)
        response = self.vision_client.document_text_detection(image=image)
        
        if response.error.message:
            raise Exception(response.error.message)
        
        return response.full_text_annotation.text
    
    def _gemini_vision_extract(self, image_bytes: bytes, raw_text: Optional[str] = None) -> Dict:
        """
        Use Gemini Vision to extract structured LaTeX.
        
        This is the core of our "Vision-Parser Handover" pattern.
        """
        # Build prompt
        prompt = self._build_vision_prompt(raw_text)
        
        # Prepare image (V2 SDK accepts PIL Image directly)
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Generate using new Client API
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt, pil_image]
        )
        response_text = response.text.strip()
        
        # Parse response
        problem_data, confidence, needs_review = self._parse_gemini_response(response_text)
        
        return {
            "problem_data": problem_data,  # Structured JSON output
            "latex": problem_data.get("problem_text_full", "") if isinstance(problem_data, dict) else problem_data,  # Backward compat
            "confidence": confidence,
            "method": "gemini_vision" if not raw_text else "cloud_vision+gemini",
            "raw_text": raw_text,
            "needs_review": needs_review,
            "error": None
        }
    
    def _build_vision_prompt(self, raw_text: Optional[str]) -> str:
        """Build prompt for Gemini Vision - FULL TEXT EXTRACTION."""
        base_prompt = """You are a mathematical OCR expert. Extract the COMPLETE problem from this image.

**CRITICAL: Extract EVERYTHING, not just equations**:
1. Problem statement (the scenario/word problem description)
2. Given information (equations, values, constraints)
3. The question being asked (find/calculate/prove what?)
4. Any additional context

**Output Format** (JSON):
{
  "problem_text_full": "Complete problem statement including all text",
  "given_values": ["equation1", "equation2", ...],
  "question": "What is being asked (find X, calculate Y, etc.)",
  "problem_type_hint": "algebra/calculus/probability/geometry/etc."
}

**Examples**:

Image: "Solve x² + 3x - 4 = 0 for x"
Output:
{
  "problem_text_full": "Solve x² + 3x - 4 = 0 for x",
  "given_values": ["x² + 3x - 4 = 0"],
  "question": "Solve for x",
  "problem_type_hint": "algebra"
}

Image: "Three students can solve a problem with probabilities 1/3, 1/10, 1/12. Find P(at least one solves)"
Output:
{
  "problem_text_full": "Three students S₁, S₂, S₃ can solve a problem. P(S₁) = 1/3, P(S₂) = 1/10, P(S₃) = 1/12. Find probability that at least one solves the problem.",
  "given_values": ["P(S₁) = 1/3", "P(S₂) = 1/10", "P(S₃) = 1/12"],
  "question": "Find P(at least one student solves)",
  "problem_type_hint": "probability"
}

**If image is unclear**: Output {"problem_text_full": "UNCLEAR: <reason>"}
"""
        
        if raw_text:
            base_prompt += f"\n\n**Hint (raw OCR, may contain errors)**:\n{raw_text}\n\nUse this as reference but extract everything from the image."
        
        return base_prompt
    
    def _parse_gemini_response(self, response_text: str) -> tuple:
        """
        Parse Gemini's JSON response.
        
        Returns:
            (problem_dict, confidence_score, needs_review)
        """
        import json
        import re
        
        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            problem_data = json.loads(cleaned)
            
            # Check if unclear
            if "UNCLEAR" in problem_data.get("problem_text_full", ""):
                return problem_data, 0.0, True
            
            # Calculate confidence
            confidence = self._calculate_confidence_structured(problem_data)
            needs_review = confidence < 0.7
            
            return problem_data, confidence, needs_review
            
        except json.JSONDecodeError:
            # Fallback: treat as plain text (old format compatibility)
            return {
                "problem_text_full": response_text,
                "given_values": [],
                "question": "Unknown",
                "problem_type_hint": "unknown"
            }, 0.5, True
    
    def _calculate_confidence_structured(self, problem_data: dict) -> float:
        """Calculate confidence from structured problem data."""
        confidence = 0.5  # Base
        
        # Has full problem text (+0.2)
        if problem_data.get("problem_text_full") and len(problem_data["problem_text_full"]) > 20:
            confidence += 0.2
        
        # Has given values (+0.1)
        if problem_data.get("given_values"):
            confidence += 0.1
        
        # Has clear question (+0.1)
        if problem_data.get("question") and problem_data["question"] != "Unknown":
            confidence += 0.1
        
        # Has problem type (+0.1)
        if problem_data.get("problem_type_hint") and problem_data["problem_type_hint"] != "unknown":
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_confidence(self, latex: str) -> float:
        """
        Heuristic confidence calculation.
        
        Factors:
        - Length (very short might be incomplete)
        - Contains mathematical symbols
        - Proper LaTeX syntax (backslashes, braces)
        """
        if not latex or len(latex) < 3:
            return 0.3
        
        confidence = 0.5  # Base confidence
        
        # Has LaTeX commands (+0.2)
        if "\\" in latex:
            confidence += 0.2
        
        # Has proper braces (+0.1)
        if "{" in latex and "}" in latex:
            confidence += 0.1
        
        # Has math operators (+0.1)
        math_symbols = ["+", "-", "=", "^", "_", "\\int", "\\frac", "\\sum"]
        if any(sym in latex for sym in math_symbols):
            confidence += 0.1
        
        # Not too short (+0.1)
        if len(latex) > 10:
            confidence += 0.1
        
        return min(confidence, 1.0)


if __name__ == "__main__":
    # Test OCR
    ocr = MathOCR()
    
    # You would test with actual image bytes here
    print("OCR Module initialized successfully!")
    print(f"Using Cloud Vision: {ocr.use_cloud_vision}")
