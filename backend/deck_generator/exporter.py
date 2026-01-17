"""
HTML/PDF Exporter for Explanation Decks
"""

import os
from typing import Optional


class DeckExporter:
    """
    Exports generated deck HTML to files or PDF.
    """
    
    def __init__(self, output_dir: str = None):
        """Initialize exporter with output directory."""
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def to_html(self, html_content: str, filename: str = "deck.html") -> str:
        """
        Save HTML content to file.
        
        Returns:
            Path to saved file
        """
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path
    
    def to_pdf(self, html_content: str, filename: str = "deck.pdf") -> Optional[str]:
        """
        Convert HTML to PDF using WeasyPrint (if available).
        
        Returns:
            Path to saved PDF, or None if WeasyPrint not installed
        """
        try:
            from weasyprint import HTML
            
            output_path = os.path.join(self.output_dir, filename)
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        except ImportError:
            print("WeasyPrint not installed. Run: pip install weasyprint")
            return None
        except Exception as e:
            print(f"PDF export failed: {e}")
            return None
    
    def preview_in_browser(self, html_content: str) -> str:
        """
        Open HTML in default browser using temp file.
        
        Returns:
            Path to temp file
        """
        import tempfile
        import webbrowser
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.html', 
            delete=False, 
            encoding='utf-8',
            dir=self.output_dir
        ) as f:
            f.write(html_content)
            temp_path = f.name
        
        webbrowser.open(f'file://{temp_path}')
        return temp_path
