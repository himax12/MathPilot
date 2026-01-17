"""
Explanation Deck Generator - Public API
Generates Gamma AI-style HTML presentation decks from math explanations.
"""

from .generator import DeckGenerator
from .themes import THEMES

__all__ = ["DeckGenerator", "THEMES"]
