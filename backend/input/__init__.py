"""
Input Package - Multimodal input processors (OCR, ASR).
"""

from .normalizer import MathNormalizer

# OCR is optional (requires google-cloud-vision)
try:
    from .ocr import MathOCR
    _has_ocr = True
except ImportError as e:
    MathOCR = None
    _has_ocr = False

# ASR is optional (requires google-cloud-speech)
try:
    from .asr import MathASR
    _has_asr = True
except ImportError as e:
    MathASR = None
    _has_asr = False

# Build __all__ based on what's available
__all__ = ["MathNormalizer"]
if _has_ocr:
    __all__.append("MathOCR")
if _has_asr:
    __all__.append("MathASR")

