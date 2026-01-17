"""
Source loaders for JEE PYQ data.
Supports JSON, PDF extraction, and web scraping.
"""

from .json_loader import PYQLoader

__all__ = ["PYQLoader"]
