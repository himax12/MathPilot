"""
Input Package - Multimodal input processors (OCR, ASR).
"""

from .ocr import MathOCR
from .normalizer import MathNormalizer

# ASR is optional (requires google-cloud-speech)
try:
    from .asr import MathASR
    __all__ = ["MathOCR", "MathASR", "MathNormalizer"]
except ImportError:
    MathASR = None
    __all__ = ["MathOCR", "MathNormalizer"]

