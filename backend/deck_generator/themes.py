"""
Theme Configuration for Explanation Decks
Defines color palettes for dark/light modes.
"""

from typing import Dict, Any

THEMES: Dict[str, Dict[str, Any]] = {
    "dark": {
        "name": "Dark Premium",
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%)",
        "card_bg": "rgba(255, 255, 255, 0.08)",
        "card_border": "rgba(255, 255, 255, 0.12)",
        "card_shadow": "0 8px 32px rgba(0, 0, 0, 0.4)",
        "text_primary": "#ffffff",
        "text_secondary": "#a0aec0",
        "text_muted": "#718096",
        "accent": "#7f5af0",
        "accent_secondary": "#2cb67d",
        "accent_glow": "rgba(127, 90, 240, 0.25)",
        "success": "#2cb67d",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "code_bg": "rgba(0, 0, 0, 0.3)",
        "font_heading": "'Inter', 'Segoe UI', sans-serif",
        "font_body": "'Inter', 'Segoe UI', sans-serif",
        "font_code": "'Fira Code', 'Consolas', monospace",
    },
    "light": {
        "name": "Light Academic",
        "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "card_border": "rgba(0, 0, 0, 0.1)",
        "card_shadow": "0 4px 16px rgba(0, 0, 0, 0.1)",
        "text_primary": "#1a202c",
        "text_secondary": "#4a5568",
        "text_muted": "#a0aec0",
        "accent": "#6366f1",
        "accent_secondary": "#10b981",
        "accent_glow": "rgba(99, 102, 241, 0.2)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "code_bg": "rgba(0, 0, 0, 0.05)",
        "font_heading": "'Inter', 'Segoe UI', sans-serif",
        "font_body": "'Inter', 'Segoe UI', sans-serif",
        "font_code": "'Fira Code', 'Consolas', monospace",
    }
}


def get_theme(name: str = "dark") -> Dict[str, Any]:
    """Get theme by name with fallback to dark."""
    return THEMES.get(name, THEMES["dark"])
