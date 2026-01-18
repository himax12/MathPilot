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
import time

try:
    from .config import config
except ImportError:
    from config import config


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
        
        # Store API key and cache client instance
        self._api_key = config.GEMINI_API_KEY
        self._client_instance = None
        # Reverting to Flash model to avoid 429 Resource Exhausted errors
        # relying on CoT (v7) and White-BG (v8) to maintain quality.
        self.model_name = "gemini-2.0-flash"
        
        # Google Cloud Vision (optional, falls back to Gemini-only if not configured)
        self.use_cloud_vision = False
        self.vision_client = None
        try:
            if hasattr(config, 'GOOGLE_APPLICATION_CREDENTIALS') and config.GOOGLE_APPLICATION_CREDENTIALS:
                self.vision_client = vision.ImageAnnotatorClient()
                self.use_cloud_vision = True
        except Exception:
            pass  # Fall back to Gemini-only mode
    
    @property
    def client(self):
        """Lazy-init and cache client."""
        if self._client_instance is None:
            self._client_instance = genai.Client(api_key=self._api_key)
        return self._client_instance
    
    def extract_from_image(self, image_bytes: bytes) -> Dict[str, any]:
        """
        Extract math expression from image.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dict containing 'latex', 'confidence', etc.
        """
        # 1. First pass: Cloud Vision (if enabled) for raw text hint
        raw_text = None
        if self.use_cloud_vision:
            try:
                raw_text = self._cloud_vision_ocr(image_bytes)
            except Exception as e:
                print(f"Cloud Vision failed (fallback to Gemini-only): {e}")
        
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
        
        # SAFETY: Force convert to RGB with WHITE background to prevent transparency issues
        # (e.g. black text on transparent bg becomes invisible if model uses black matte)
        if pil_image.mode in ('RGBA', 'LA') or (pil_image.mode == 'P' and 'transparency' in pil_image.info):
            background = Image.new('RGB', pil_image.size, (255, 255, 255))
            if pil_image.mode == 'P':
                pil_image = pil_image.convert('RGBA')
            background.paste(pil_image, mask=pil_image.split()[-1])
            pil_image = background
        elif pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Generate using new Client API
        # Retry logic for 429 Resource Exhausted
        max_retries = 3
        response = None
        
        # Configure for detailed output
        from google.genai import types
        gen_config = types.GenerateContentConfig(
            max_output_tokens=2048,
            temperature=0.1 # Low temp for faithful transcription
        )
        
        # Safety settings - BLOCK_NONE to prevent silent truncation
        # The new SDK might use different enums, but let's try the standard dict format first which usually works
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, pil_image],
                    config=gen_config,
                    # safety_settings=safety_settings # Commented out for now as SDK V2 uses different types in python 
                    # We will rely on the prompt being benign math. 
                    # Actually, let's try to pass it if the SDK supports it.
                    # Based on google-genai, it might be part of config.
                )
                break
            except Exception as e:
                # Check for 429
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries - 1:
                        wait = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s
                        print(f"⚠️ Rate limit hit (429). Retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                # If not 429 or retries exhausted, re-raise
                raise e
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
        """Build prompt for Gemini Vision - CHAIN OF THOUGHT EXTRACTION."""
        base_prompt = """You are a specialized Mathematical OCR agent.
        
TASK:
Perform a 2-step transcription of this image.

STEP 1: SCANNING
- Look at the bottom of the image. Are there multiple choice options (A, B, C, D)?
- Are there any graphs or diagrams?

STEP 2: TRANSCRIPTION
- Transcribe the FULL text of the problem.
- IF you saw options in Step 1, you MUST list them exactly as they appear.
- Write equations in LaTeX.

**OUTPUT FORMAT**:
Just the final transcription. Do not output your "scanning" thought process, just the result. Ensure the OPTIONS are included at the bottom.

**Example**:
Calculate the area of the circle.

A) 2pi
B) 4pi
C) pi
D) 8pi
"""
        
        if raw_text:
            base_prompt += f"\n\n**Hint (raw OCR)**:\n{raw_text}\n"
        
        return base_prompt
    
    def _parse_gemini_response(self, response_text: str) -> tuple:
        """
        Parse Gemini's response.
        """
        # Clean up any potential markdown code blocks wrapper
        cleaned = response_text.replace("```markdown", "").replace("```", "").strip()
        
        # Check if unclear
        if "UNCLEAR" in cleaned:
             return {
                "problem_text_full": cleaned,
                "needs_review": True
            }, 0.0, True
            
        # Structure it simply for compatibility
        problem_data = {
            "problem_text_full": cleaned,
            "given_values": [],
            "question": "See problem text",
            "options": [],
            "problem_type_hint": "general"
        }
        
        # Simple confidence heuristic
        confidence = 0.8 if len(cleaned) > 10 else 0.4
        needs_review = confidence < 0.6
        
        return problem_data, confidence, needs_review
    
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
