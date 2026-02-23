"""
Centralized Configuration for Math Mentor
All settings, thresholds, and model names in one place.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root (parent of backend/)
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")


class Config:
    """
    Centralized configuration management.
    
    Values are loaded from environment variables with sensible defaults.
    This eliminates hardcoded values scattered across the codebase.
    """
    
    # ==========================================================
    # API CONFIGURATION
    # ==========================================================
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    GEMINI_MODEL_FLASH: str = os.getenv("GEMINI_MODEL_FLASH", "gemini-2.5-pro")
    GEMINI_VISION_MODEL: str = os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-pro")
    
    # Google Cloud (Vertex AI / Vision / STT)
    USE_VERTEX_AI: bool = os.getenv("USE_VERTEX_AI", "false").lower() == "true"
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_PROJECT_ID", "")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    
    # Google Speech-to-Text V2 (Chirp 2)
    STT_LOCATION: str = os.getenv("STT_LOCATION", "global")  # Changed to global for compatibility
    STT_RECOGNIZER: str = os.getenv("STT_RECOGNIZER", "_") # Use "_" for default recognizer
    
    # ==========================================================
    # EXECUTION SETTINGS
    # ==========================================================
    
    # Executor
    EXECUTOR_TIMEOUT_SECONDS: int = int(os.getenv("EXECUTOR_TIMEOUT", "5"))
    MAX_PLOTS_TO_DISPLAY: int = int(os.getenv("MAX_PLOTS", "3"))
    
    # ==========================================================
    # CONFIDENCE THRESHOLDS
    # ==========================================================
    
    # OCR confidence thresholds
    OCR_CONFIDENCE_HIGH: float = float(os.getenv("OCR_CONFIDENCE_HIGH", "0.8"))
    OCR_CONFIDENCE_MEDIUM: float = float(os.getenv("OCR_CONFIDENCE_MEDIUM", "0.5"))
    
    # Parser confidence
    PARSER_BASE_CONFIDENCE: float = float(os.getenv("PARSER_BASE_CONFIDENCE", "0.5"))
    
    # HITL (Human-in-the-Loop) review threshold
    HITL_REVIEW_THRESHOLD: float = float(os.getenv("HITL_THRESHOLD", "0.7"))
    
    # ==========================================================
    # UI SETTINGS
    # ==========================================================
    
    APP_TITLE: str = os.getenv("APP_TITLE", "Math Mentor")
    APP_ICON: str = os.getenv("APP_ICON", "🧮")
    APP_SUBTITLE: str = os.getenv("APP_SUBTITLE", "AI-powered math problem solver with OCR + Program-of-Thoughts")
    
    # ==========================================================
    # DECK GENERATOR SETTINGS
    # ==========================================================
    
    DECK_DEFAULT_THEME: str = os.getenv("DECK_THEME", "dark")
    KATEX_CDN_URL: str = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist"
    
    # ==========================================================
    # ALLOWED MODULES IN SANDBOX
    # ==========================================================
    
    SANDBOX_ALLOWED_MODULES: tuple = (
        "math",
        "sympy",
        "numpy",
        "matplotlib",
        "matplotlib.pyplot",
    )
    
    # ==========================================================
    # VALIDATION
    # ==========================================================
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        errors = []
        
        if not cls.GEMINI_API_KEY and not cls.USE_VERTEX_AI:
            errors.append("GEMINI_API_KEY is required when USE_VERTEX_AI is false")
        
        if cls.USE_VERTEX_AI and not cls.GCP_PROJECT_ID:
            errors.append("GCP_PROJECT_ID is required when USE_VERTEX_AI is true")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def summary(cls) -> str:
        """Return a summary of current configuration (for logging)."""
        return f"""
Math Mentor Configuration:
  - Model: {cls.GEMINI_MODEL}
  - Use Vertex AI: {cls.USE_VERTEX_AI}
  - Executor Timeout: {cls.EXECUTOR_TIMEOUT_SECONDS}s
  - OCR High Confidence: {cls.OCR_CONFIDENCE_HIGH}
  - HITL Threshold: {cls.HITL_REVIEW_THRESHOLD}
  - Deck Theme: {cls.DECK_DEFAULT_THEME}
"""


# Singleton instance for easy import
config = Config()
