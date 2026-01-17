"""
Async Diagram Generator
Creates hand-drawn style diagrams for math explanations.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Any
import hashlib
import os


class DiagramGenerator:
    """
    Generates hand-drawn style diagrams asynchronously.
    Uses matplotlib's xkcd mode for sketchy aesthetics.
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize with optional cache directory."""
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def generate_async(self, diagram_type: str, params: Dict[str, Any] = None) -> str:
        """
        Generate diagram asynchronously, returns base64 encoded image.
        
        Args:
            diagram_type: Type of diagram (parabola, triangle, number_line, etc.)
            params: Parameters for the specific diagram type
        
        Returns:
            Base64 encoded PNG image string
        """
        future = self.executor.submit(self._generate, diagram_type, params or {})
        return future.result()  # Wait for completion
    
    def _generate(self, diagram_type: str, params: Dict[str, Any]) -> str:
        """Internal: Generate diagram synchronously."""
        # Check cache first
        cache_key = self._cache_key(diagram_type, params)
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        # Generate based on type
        generators = {
            "parabola": self._draw_parabola,
            "triangle": self._draw_triangle,
            "number_line": self._draw_number_line,
            "coordinate_plane": self._draw_coordinate_plane,
            "unit_circle": self._draw_unit_circle,
            "generic": self._draw_generic,
        }
        
        generator = generators.get(diagram_type, self._draw_generic)
        image_data = generator(params)
        
        # Cache result
        self._set_cached(cache_key, image_data)
        return image_data
    
    def _cache_key(self, diagram_type: str, params: Dict) -> str:
        """Generate cache key from type and params."""
        content = f"{diagram_type}:{sorted(params.items())}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached(self, key: str) -> Optional[str]:
        """Retrieve from cache if exists."""
        cache_path = os.path.join(self.cache_dir, f"{key}.b64")
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return f.read()
        return None
    
    def _set_cached(self, key: str, data: str):
        """Save to cache."""
        cache_path = os.path.join(self.cache_dir, f"{key}.b64")
        with open(cache_path, 'w') as f:
            f.write(data)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 PNG."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                    facecolor='#1a1a2e', edgecolor='none')
        buf.seek(0)
        data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return data
    
    def _draw_parabola(self, params: Dict) -> str:
        """Draw a parabola (quadratic function)."""
        a = params.get('a', 1)
        b = params.get('b', 0)
        c = params.get('c', 0)
        
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.set_facecolor('#1a1a2e')
            
            x = np.linspace(-10, 10, 200)
            y = a * x**2 + b * x + c
            
            ax.plot(x, y, color='#7f5af0', linewidth=2.5, label=f'y = {a}x² + {b}x + {c}')
            ax.axhline(y=0, color='#a0aec0', linestyle='-', linewidth=0.8)
            ax.axvline(x=0, color='#a0aec0', linestyle='-', linewidth=0.8)
            ax.grid(True, alpha=0.2, color='#a0aec0')
            ax.set_xlabel('x', color='#ffffff', fontsize=12)
            ax.set_ylabel('y', color='#ffffff', fontsize=12)
            ax.tick_params(colors='#a0aec0')
            ax.legend(facecolor='#16213e', edgecolor='#7f5af0', labelcolor='#ffffff')
            ax.set_ylim(-20, 50)
            
            for spine in ax.spines.values():
                spine.set_color('#a0aec0')
        
        return self._fig_to_base64(fig)
    
    def _draw_triangle(self, params: Dict) -> str:
        """Draw a triangle with labeled sides."""
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.set_facecolor('#1a1a2e')
            
            # Default triangle vertices
            vertices = params.get('vertices', [(0, 0), (4, 0), (2, 3)])
            vertices.append(vertices[0])  # Close the triangle
            
            xs, ys = zip(*vertices)
            ax.plot(xs, ys, color='#7f5af0', linewidth=2.5)
            ax.fill(xs, ys, alpha=0.2, color='#7f5af0')
            
            # Labels
            labels = params.get('labels', ['A', 'B', 'C'])
            for i, (x, y) in enumerate(vertices[:-1]):
                ax.annotate(labels[i], (x, y), fontsize=14, color='#2cb67d',
                           xytext=(5, 5), textcoords='offset points')
            
            ax.set_aspect('equal')
            ax.axis('off')
        
        return self._fig_to_base64(fig)
    
    def _draw_number_line(self, params: Dict) -> str:
        """Draw a number line with marked points."""
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.set_facecolor('#1a1a2e')
            
            start = params.get('start', -5)
            end = params.get('end', 5)
            points = params.get('points', [])
            
            ax.axhline(y=0, color='#a0aec0', linewidth=2)
            ax.set_xlim(start - 0.5, end + 0.5)
            ax.set_ylim(-0.5, 0.5)
            
            for i in range(start, end + 1):
                ax.plot([i, i], [-0.1, 0.1], color='#a0aec0', linewidth=1.5)
                ax.text(i, -0.3, str(i), ha='center', color='#a0aec0', fontsize=10)
            
            for p in points:
                ax.plot(p, 0, 'o', color='#7f5af0', markersize=12)
            
            ax.axis('off')
        
        return self._fig_to_base64(fig)
    
    def _draw_coordinate_plane(self, params: Dict) -> str:
        """Draw a coordinate plane with optional points."""
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.set_facecolor('#1a1a2e')
            
            ax.axhline(y=0, color='#a0aec0', linewidth=1.5)
            ax.axvline(x=0, color='#a0aec0', linewidth=1.5)
            ax.grid(True, alpha=0.2, color='#a0aec0')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_aspect('equal')
            ax.tick_params(colors='#a0aec0')
            
            points = params.get('points', [])
            for (x, y, label) in points:
                ax.plot(x, y, 'o', color='#7f5af0', markersize=10)
                ax.annotate(label, (x, y), color='#2cb67d', fontsize=12,
                           xytext=(5, 5), textcoords='offset points')
            
            for spine in ax.spines.values():
                spine.set_color('#a0aec0')
        
        return self._fig_to_base64(fig)
    
    def _draw_unit_circle(self, params: Dict) -> str:
        """Draw unit circle for trigonometry."""
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.set_facecolor('#1a1a2e')
            
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(theta), np.sin(theta), color='#7f5af0', linewidth=2)
            
            ax.axhline(y=0, color='#a0aec0', linewidth=1)
            ax.axvline(x=0, color='#a0aec0', linewidth=1)
            
            # Mark key angles
            angles = params.get('angles', [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
            for angle in angles:
                x, y = np.cos(angle), np.sin(angle)
                ax.plot([0, x], [0, y], color='#2cb67d', linewidth=1.5)
                ax.plot(x, y, 'o', color='#2cb67d', markersize=8)
            
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect('equal')
            ax.axis('off')
        
        return self._fig_to_base64(fig)
    
    def _draw_generic(self, params: Dict) -> str:
        """Draw a generic placeholder diagram."""
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.set_facecolor('#1a1a2e')
            
            ax.text(0.5, 0.5, params.get('text', 'Diagram'), 
                   ha='center', va='center', fontsize=20, color='#7f5af0',
                   transform=ax.transAxes)
            ax.axis('off')
        
        return self._fig_to_base64(fig)
    
    def shutdown(self):
        """Shutdown the thread pool."""
        self.executor.shutdown(wait=False)


# Singleton instance
_diagram_generator: Optional[DiagramGenerator] = None


def get_diagram_generator() -> DiagramGenerator:
    """Get or create the singleton diagram generator."""
    global _diagram_generator
    if _diagram_generator is None:
        _diagram_generator = DiagramGenerator()
    return _diagram_generator
