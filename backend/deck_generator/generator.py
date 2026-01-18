"""
Core Deck Generator
Transforms structured math explanations into HTML presentation decks.
"""

import re
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from jinja2 import Environment, FileSystemLoader, BaseLoader
from .themes import get_theme, THEMES
from .diagrams import get_diagram_generator
from .models import MathDeck, MathSlide, VisualRequest


# ============================================================================
# CONFIGURABLE PATTERNS (No hardcoding!)
# ============================================================================

SECTION_PATTERNS = {
    # Intuition section patterns (try in order)
    "intuition": [
        r"\*\*INTUITION\*\*[:\s]*(.+?)(?=\*\*SOLUTION|\*\*STEP|\*\*CODE|\*\*VIS|$)",
        r"💡\s*\*?\*?Intuition\*?\*?[:\s]*(.+?)(?=\*\*|$)",
        r"Key\s*Insight[:\s]*(.+?)(?=\*\*|Step|$)",
        r"Overview[:\s]*(.+?)(?=\*\*|Step|$)",
    ],
    # Solution steps section (outer container)
    "steps_section": [
        r"\*\*SOLUTION STEPS\*\*[:\s]*(.+?)(?=\*\*CODE|\*\*VIS|\*\*EXPLANATION|$)",
        r"\*\*Steps\*\*[:\s]*(.+?)(?=\*\*CODE|$)",
        r"Step-by-Step[:\s]*(.+?)(?=Code|$)",
    ],
    # Individual step patterns
    "step_item": [
        r"\*\*Step\s*(\d+)\*\*[:\s]*(.+?)(?=\*\*Step|\*\*CODE|\*\*VIS|$)",
        r"Step\s*(\d+)[:\s]+(.+?)(?=Step\s*\d|Code|$)",
        r"(\d+)\.\s+(.+?)(?=\d+\.|$)",
    ],
    # Visualization section
    "visualization": [
        r"\*\*VISUALIZATION\*\*[:\s]*(.+?)(?=\*\*CODE|```|$)",
        r"📊\s*(.+?)(?=\*\*|```|$)",
        r"Diagram[:\s]*(.+?)(?=\*\*|```|$)",
    ],
    # Answer/Explanation section
    "explanation": [
        r"\*\*EXPLANATION\*\*[:\s]*(.+?)(?=$)",
        r"\*\*ANSWER\*\*[:\s]*(.+?)(?=$)",
        r"Final\s*Answer[:\s]*(.+?)(?=$)",
    ],
    # LaTeX patterns for rendering
    "latex_inline": [
        r"\$([^$]+)\$",
        r"\\\((.+?)\\\)",
    ],
    "latex_block": [
        r"\$\$(.+?)\$\$",
        r"\\\[(.+?)\\\]",
    ],
}


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Slide:
    """Represents a single slide in the deck."""
    slide_type: str  # title, intuition, step, visualization, answer
    title: str = ""
    content: str = ""
    diagram: Optional[str] = None  # Base64 image data
    latex_blocks: List[str] = field(default_factory=list)
    step_number: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Deck:
    """Represents the complete presentation deck."""
    title: str
    slides: List[Slide] = field(default_factory=list)
    theme: str = "dark"
    answer: str = ""
    

# ============================================================================
# FLEXIBLE PARSER
# ============================================================================

class ReasoningParser:
    """
    Flexible parser for extracting structured data from reasoning text.
    Uses configurable patterns with fallback chains.
    """
    
    def __init__(self, patterns: Dict[str, List[str]] = None):
        self.patterns = patterns or SECTION_PATTERNS
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse reasoning text into structured data.
        
        Returns:
            Dict with keys: intuition, steps, visualization, explanation, etc.
        """
        result = {
            "intuition": "",
            "steps": [],
            "visualization": "",
            "explanation": "",
            "raw": text,
        }
        
        # Clean text
        text = text.strip()
        
        # Extract intuition
        result["intuition"] = self._extract_section(text, "intuition")
        
        # Extract steps
        result["steps"] = self._extract_steps(text)
        
        # Extract visualization text
        result["visualization"] = self._extract_section(text, "visualization")
        
        # Extract explanation/answer
        result["explanation"] = self._extract_section(text, "explanation")
        
        return result
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a section using pattern fallback chain."""
        patterns = self.patterns.get(section_name, [])
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_steps(self, text: str) -> List[Dict[str, str]]:
        """Extract individual steps from the text."""
        steps = []
        patterns = self.patterns.get("step_item", [])
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        steps.append({
                            "number": int(match[0]) if match[0].isdigit() else len(steps) + 1,
                            "content": match[1].strip()
                        })
                    elif isinstance(match, str):
                        steps.append({
                            "number": len(steps) + 1,
                            "content": match.strip()
                        })
                
                if steps:
                    break  # Use first pattern that matches
        
        return steps
    
    def extract_latex(self, text: str) -> List[str]:
        """Extract all LaTeX expressions from text."""
        latex_items = []
        
        # Inline LaTeX
        for pattern in self.patterns.get("latex_inline", []):
            matches = re.findall(pattern, text, re.DOTALL)
            latex_items.extend(matches)
        
        # Block LaTeX
        for pattern in self.patterns.get("latex_block", []):
            matches = re.findall(pattern, text, re.DOTALL)
            latex_items.extend(matches)
        
        return latex_items


# ============================================================================
# DECK GENERATOR
# ============================================================================

class DeckGenerator:
    """
    Main class for generating explanation decks.
    """
    
    def __init__(self, theme: str = "dark", patterns: Dict[str, List[str]] = None):
        """
        Initialize the deck generator.
        
        Args:
            theme: Color theme name ('dark' or 'light')
            patterns: Custom section patterns (optional)
        """
        self.theme = get_theme(theme)
        self.theme_name = theme
        self.parser = ReasoningParser(patterns)
        self.diagram_gen = get_diagram_generator()
        
        # Setup Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        if os.path.exists(template_dir):
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        else:
            # Fallback to string-based template
            self.jinja_env = Environment(loader=BaseLoader())
    
    def generate(
        self,
        title: str,
        intuition: str = "",
        steps: List[Dict[str, str]] = None,
        answer: str = "",
        visualization: str = "",
        domain: str = "algebra"
    ) -> str:
        """
        Generate HTML deck from structured input.
        
        Returns:
            HTML string of the complete deck
        """
        slides = []
        
        # Title slide
        slides.append(Slide(
            slide_type="title",
            title=title,
            content=f"Domain: {domain.capitalize()}"
        ))
        
        # Intuition slide
        if intuition:
            slides.append(Slide(
                slide_type="intuition",
                title="💡 Key Insight",
                content=intuition
            ))
        
        # Step slides
        for step in (steps or []):
            step_num = step.get("number", len(slides))
            slides.append(Slide(
                slide_type="step",
                title=f"Step {step_num}",
                content=step.get("content", ""),
                step_number=step_num,
                latex_blocks=self.parser.extract_latex(step.get("content", ""))
            ))
        
        # Visualization slide (auto-generate diagram if geometry)
        if visualization or domain == "geometry":
            diagram = None
            if domain == "geometry":
                diagram = self.diagram_gen.generate_async("triangle", {})
            elif domain == "algebra":
                diagram = self.diagram_gen.generate_async("parabola", {"a": 1, "b": 0, "c": 0})
            
            slides.append(Slide(
                slide_type="visualization",
                title="📊 Visual Explanation",
                content=visualization,
                diagram=diagram
            ))
        
        # Answer slide
        if answer:
            slides.append(Slide(
                slide_type="answer",
                title="🎯 Final Answer",
                content=answer
            ))
        
        # Create deck
        deck = Deck(title=title, slides=slides, theme=self.theme_name, answer=answer)
        
        return self._render_html(deck)
    
    def from_structured(self, deck_data: MathDeck) -> str:
        """
        Generate HTML deck from structured MathDeck model (Pydantic).
        Preferred entry point for Phase 3.
        """
        slides = []
        
        # Convert Pydantic slides to internal Slide objects
        for i, slide in enumerate(deck_data.slides):
            diagram_b64 = None
            if slide.visual_request:
                # Agent explicitly requested a visualization
                # Build params from individual fields
                params = {}
                if slide.visual_request.a is not None:
                    params['a'] = slide.visual_request.a
                if slide.visual_request.b is not None:
                    params['b'] = slide.visual_request.b
                if slide.visual_request.c is not None:
                    params['c'] = slide.visual_request.c
                    
                diagram_b64 = self.diagram_gen.generate_async(
                    slide.visual_request.type,
                    params
                )
            
            # Extract LaTeX from content (reusing existing logic)
            latex_blocks = self.parser.extract_latex(slide.content)
            
            slides.append(Slide(
                slide_type=slide.type,
                title=slide.title,
                content=slide.content,
                diagram=diagram_b64,
                latex_blocks=latex_blocks,
                step_number=slide.step_number or (i if slide.type == 'step' else None)
            ))
            
        deck = Deck(
            title=deck_data.title,
            slides=slides,
            theme=self.theme_name,
            answer=deck_data.final_answer
        )
        
        return self._render_html(deck)

    def from_reasoning_text(self, raw_text: str, answer: str = "", title: str = "Math Solution") -> str:
        """
        Generate HTML deck by parsing raw reasoning text.
        
        This is the primary entry point when using with the Solver output.
        """
        parsed = self.parser.parse(raw_text)
        
        return self.generate(
            title=title,
            intuition=parsed["intuition"],
            steps=parsed["steps"],
            answer=answer or parsed["explanation"],
            visualization=parsed["visualization"]
        )

    
    def _render_html(self, deck: Deck) -> str:
        """Render the deck to HTML."""
        try:
            template = self.jinja_env.get_template("deck.html")
            return template.render(deck=deck, theme=self.theme)
        except Exception:
            # Fallback to embedded template
            return self._render_embedded_template(deck)
    
    def _render_embedded_template(self, deck: Deck) -> str:
        """Fallback: render using embedded template string."""
        theme = self.theme
        
        slides_html = ""
        for i, slide in enumerate(deck.slides):
            slides_html += f'''
            <section class="slide slide-{slide.slide_type}" data-index="{i}">
                <div class="slide-card">
                    <h2 class="slide-title">{slide.title}</h2>
                    <div class="slide-content">
                        {self._format_content(slide.content)}
                    </div>
                    {f'<img src="data:image/png;base64,{slide.diagram}" class="slide-diagram" />' if slide.diagram else ''}
                </div>
            </section>
            '''
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{deck.title}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: {theme["font_body"]};
            background: {theme["bg_gradient"]};
            color: {theme["text_primary"]};
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .deck-container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .deck-title {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, {theme["accent"]} 0%, {theme["accent_secondary"]} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .slide {{
            margin-bottom: 2rem;
        }}
        
        .slide-card {{
            background: {theme["card_bg"]};
            border: 1px solid {theme["card_border"]};
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            box-shadow: {theme["card_shadow"]};
        }}
        
        .slide-title {{
            color: {theme["accent"]};
            font-size: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }}
        
        .slide-content {{
            line-height: 1.8;
            color: {theme["text_secondary"]};
        }}
        
        .slide-content p {{
            margin-bottom: 0.5rem;
        }}
        
        .slide-diagram {{
            max-width: 100%;
            border-radius: 8px;
            margin-top: 1rem;
        }}
        
        .slide-answer .slide-card {{
            border-color: {theme["success"]};
            box-shadow: 0 0 30px {theme["accent_glow"]};
        }}
        
        .slide-answer .slide-content {{
            font-size: 1.5rem;
            color: {theme["success"]};
            text-align: center;
            font-weight: 600;
        }}
        
        /* Progress indicator */
        .progress {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 2rem;
        }}
        
        .progress-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: {theme["card_border"]};
        }}
        
        .progress-dot.active {{
            background: {theme["accent"]};
        }}
    </style>
</head>
<body>
    <div class="deck-container">
        <h1 class="deck-title">{deck.title}</h1>
        {slides_html}
        <div class="progress">
            {''.join([f'<span class="progress-dot{" active" if i == 0 else ""}"></span>' for i in range(len(deck.slides))])}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script>
        // Auto-render LaTeX
        document.querySelectorAll('.slide-content').forEach(el => {{
            const text = el.innerHTML;
            el.innerHTML = text.replace(/\\$(.+?)\\$/g, (match, latex) => {{
                try {{
                    return katex.renderToString(latex, {{ throwOnError: false }});
                }} catch (e) {{
                    return match;
                }}
            }});
        }});
    </script>
</body>
</html>'''
        
        return html
    
    def _format_content(self, content: str) -> str:
        """Format content with markdown-like processing."""
        # Convert line breaks
        content = content.replace("\n", "<br>")
        
        # Bold
        content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
        
        # Bullet points (basic)
        content = re.sub(r"^- (.+)$", r"<p>• \1</p>", content, flags=re.MULTILINE)
        
        return content
    
    def to_html_file(self, html: str, output_path: str) -> str:
        """Save HTML to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path
    
    def preview(self, html: str):
        """Open HTML in default browser."""
        import tempfile
        import webbrowser
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        
        webbrowser.open(f'file://{temp_path}')
        return temp_path

    def render_context(self, context_str: str) -> str:
        """
        Render RAG context as structured HTML carousel.
        
        Args:
            context_str: Raw context string, typically formatted as:
                         "--- Source 1: topic > subtopic (Relevance: X%) ---\\n...content..."
                         
        Returns:
            HTML string of the context deck
        """
        import markdown
        
        sources = []
        
        # Split by source delimiter (handles both Frequency and Relevance patterns)
        source_pattern = r"---\s*Source\s*(\d+):\s*(.+?)\s*\((?:Frequency|Relevance):\s*[\d.%]+\)\s*---"
        
        # Find all source headers and their positions
        matches = list(re.finditer(source_pattern, context_str))
        
        for idx, match in enumerate(matches):
            source_num = match.group(1)
            title = match.group(2).strip()
            
            # Get content between this header and the next (or end of string)
            start_pos = match.end()
            end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(context_str)
            content = context_str[start_pos:end_pos].strip()
            
            # Strip YAML frontmatter (between --- and ---)
            if content.startswith("---"):
                # Find the closing ---
                frontmatter_end = content.find("---", 3)
                if frontmatter_end != -1:
                    # Skip past the closing --- and any newlines
                    content = content[frontmatter_end + 3:].strip()
            
            # Skip the header line if it starts with "# " (it's part of the doc)
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                # Skip metadata-like lines
                if line.strip().startswith('chapter:') or line.strip().startswith('topic:'):
                    continue
                if line.strip().startswith('jee_frequency:') or line.strip().startswith('years_appeared:'):
                    continue
                if line.strip().startswith('question_count:') or line.strip().startswith('difficulty:'):
                    continue
                cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines).strip()
            
            # Convert markdown to HTML
            try:
                html_content = markdown.markdown(content, extensions=['extra', 'nl2br'])
            except Exception:
                html_content = self._format_content(content)
            
            sources.append({
                "title": title,
                "content": html_content
            })
        
        # Fallback if no sources parsed (single block of text)
        if not sources and context_str.strip():
            # Strip everything before the main content
            display_content = context_str.strip()
            
            # Remove YAML frontmatter
            if "---" in display_content:
                parts = display_content.split("---")
                if len(parts) >= 3:
                    display_content = "---".join(parts[2:]).strip()
            
            try:
                html_content = markdown.markdown(display_content, extensions=['extra', 'nl2br'])
            except Exception:
                html_content = self._format_content(display_content)
            
            sources.append({
                "title": "Retrieved Knowledge",
                "content": html_content
            })
        
        # Render template
        try:
            template = self.jinja_env.get_template("context_deck.html")
            return template.render(sources=sources, source_count=len(sources))
        except Exception as e:
            # Fallback: simple HTML
            return f"<div style='background:#1a1a2e;color:#fff;padding:1rem;'><pre>{context_str}</pre></div>"
