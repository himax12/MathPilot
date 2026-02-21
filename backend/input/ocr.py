"""
OCR Module - Extracts math expressions from images.
Uses Google Cloud Vision + Gemini Vision for robust extraction.
"""

from google import genai
from google.cloud import vision
import base64
from typing import Dict, Optional
from PIL import Image
import io
try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

from backend.config import config


class MathOCR:
    """
    Extracts mathematical expressions from images using dual-model approach:
    1. Google Cloud Vision (fast, good for printed text)
    2. Gemini Vision (semantic understanding, repairs OCR errors)
    """
    
    def __init__(self):
        """Initialize OCR clients."""
        # Gemini Vision for semantic LaTeX extraction
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = config.GEMINI_VISION_MODEL
        
        # Google Cloud Vision (optional, falls back to Gemini-only if not configured)
        self.use_cloud_vision = False
        try:
            if config.GOOGLE_APPLICATION_CREDENTIALS:
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
            # Fallback to Tesseract if both Cloud Vision and Gemini fail (or local offline mode)
            try:
                print(f"Gemini Vision failed: {e}, falling back to Tesseract")
                if not HAS_TESSERACT:
                    raise Exception("pytesseract is not installed")
                pil_image = Image.open(io.BytesIO(image_bytes))
                tesseract_text = pytesseract.image_to_string(pil_image).strip()
                if not tesseract_text:
                    raise Exception("Tesseract returned empty string")
                return {
                    "problem_data": {"problem_text_full": tesseract_text, "given_values": [], "question": "Unknown", "problem_type_hint": "unknown", "confidence": 0.3},
                    "latex": tesseract_text,
                    "confidence": 0.3, # Low confidence for raw tesseract
                    "method": "pytesseract",
                    "raw_text": raw_text or tesseract_text,
                    "needs_review": True,
                    "error": None
                }
            except Exception as tess_e:
                return {
                    "latex": None,
                    "confidence": 0.0,
                    "method": "failed",
                    "raw_text": raw_text,
                    "needs_review": True,
                    "error": f"All OCR methods failed. Last error (Tesseract): {tess_e}"
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

**CRITICAL: Extract EVERYTHING exactly as it appears (including all text and math)**:
1. Problem statement (the scenario/word problem description)
2. Given information (equations, values, constraints)
3. The question being asked (find/calculate/prove what?)
4. Multiple-choice options (e.g., (A), (B), (C), (D)), if present.
5. Any additional context

**Output Format** (JSON):
{
  "problem_text_full": "Complete problem statement including all text, math, AND multiple-choice options exactly as written",
  "given_values": ["equation1", "equation2", ...],
  "question": "What is being asked (find X, calculate Y, etc.)",
  "problem_type_hint": "algebra/calculus/probability/geometry/etc.",
  "confidence": 0.95 // Explicitly rate your extraction confidence from 0.0 to 1.0 based on image clarity
}

**Examples**:

Image: "Solve x² + 3x - 4 = 0 for x"
Output:
{
  "problem_text_full": "Solve x² + 3x - 4 = 0 for x",
  "given_values": ["x² + 3x - 4 = 0"],
  "question": "Solve for x",
  "problem_type_hint": "algebra",
  "confidence": 0.95
}

Image: "What is the value of 2 + 2?\\n(A) 3\\n(B) 4\\n(C) 5\\n(D) 6"
Output:
{
  "problem_text_full": "What is the value of 2 + 2?\\n(A) 3\\n(B) 4\\n(C) 5\\n(D) 6",
  "given_values": ["2 + 2"],
  "question": "What is the value?",
  "problem_type_hint": "algebra",
  "confidence": 0.99
}

Image: "Three students can solve a problem with probabilities 1/3, 1/10, 1/12. Find P(at least one solves)"
Output:
{
  "problem_text_full": "Three students S₁, S₂, S₃ can solve a problem. P(S₁) = 1/3, P(S₂) = 1/10, P(S₃) = 1/12. Find probability that at least one solves the problem.",
  "given_values": ["P(S₁) = 1/3", "P(S₂) = 1/10", "P(S₃) = 1/12"],
  "question": "Find P(at least one student solves)",
  "problem_type_hint": "probability",
  "confidence": 0.90
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
                "problem_type_hint": "unknown",
                "confidence": 0.5
            }, 0.5, True
    
    def _calculate_confidence_structured(self, problem_data: dict) -> float:
        """Use the LLM's self-reported confidence, or fallback."""
        try:
            # Use the LLM's self-reported confidence if it provided it
            if "confidence" in problem_data:
                return float(problem_data["confidence"])
        except ValueError:
            pass
            
        # Fallback if no valid confidence was provided
        return 0.5


if __name__ == "__main__":
    # Test OCR
    ocr = MathOCR()
    
    # You would test with actual image bytes here
    print("OCR Module initialized successfully!")
    print(f"Using Cloud Vision: {ocr.use_cloud_vision}")
