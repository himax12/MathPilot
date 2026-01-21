"""
Document Generator for JEE KB Builder.
Generates comprehensive KB documents from aggregated question patterns.
"""

import asyncio
from typing import Dict, List, Optional
from pathlib import Path

from backend.config import config

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False


class DocGenerator:
    """
    Generate KB documents from aggregated questions.
    
    Creates comprehensive markdown documents with:
    - Pattern recognition guide
    - Core formulas
    - Worked examples from PYQs
    - Common mistakes and tricks
    """
    
    DOC_GENERATION_PROMPT = '''You are creating a JEE Math knowledge base document for pattern: {pattern_name}

Based on {count} questions from JEE ({years}):

{sample_questions}

Generate a comprehensive markdown document. Be specific and JEE-focused.

---
id: "{pattern_id}"
domain: "{domain}"
subtopic: "{subtopic}"
jee_frequency: "{frequency}"
jee_years: [{years}]
---

# {pattern_name}

## Pattern Recognition
[2-3 sentences on how to identify this pattern in JEE questions]

## Core Formulas
[Key formulas in LaTeX - use $...$ for inline, $$...$$ for display]

## Standard Approach
[Numbered step-by-step method]

## Worked Examples

### Example 1: JEE {first_year}
**Problem**: [First example problem]
**Solution**:
[Step-by-step solution]

### Example 2: JEE {second_year}
**Problem**: [Second example problem]
**Solution**:
[Step-by-step solution]

### Example 3: JEE {third_year}
**Problem**: [Third example problem]
**Solution**:
[Step-by-step solution]

## Variations in JEE
[How JEE varies this pattern - common twists]

## Quick Tricks
- [Time-saving shortcut 1]
- [Time-saving shortcut 2]

## Common Mistakes
- ❌ [What students do wrong]
- ✅ [What to do instead]
'''

    def __init__(self):
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai not installed. Run: uv add google-genai")
        
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = config.GEMINI_MODEL
        self._rate_limit_delay = 1.0  # seconds between requests
    
    async def generate_doc(
        self, 
        pattern_name: str, 
        questions: List[Dict],
        stats: Dict = None
    ) -> str:
        """
        Generate a KB document for a pattern.
        
        Args:
            pattern_name: Pattern key like "calculus/integration"
            questions: List of questions in this pattern
            stats: Optional stats dict from aggregator
        
        Returns:
            Markdown document string
        """
        # Extract domain/subtopic from pattern name
        parts = pattern_name.split("/")
        domain = parts[0] if len(parts) > 0 else "unknown"
        subtopic = parts[1] if len(parts) > 1 else "unknown"
        
        # Get years
        years = sorted(set(q.get("year", 0) for q in questions if q.get("year")))
        years_str = ", ".join(str(y) for y in years[-10:])  # Last 10 years
        
        # Get frequency
        frequency = stats.get("frequency", "medium") if stats else "medium"
        
        # Sample questions for examples
        sample = self._select_best_samples(questions, n=10)
        sample_text = self._format_sample_questions(sample)
        
        # Get example years
        first_year = sample[0].get("year", "recent") if sample else "recent"
        second_year = sample[1].get("year", "recent") if len(sample) > 1 else "recent"
        third_year = sample[2].get("year", "recent") if len(sample) > 2 else "recent"
        
        prompt = self.DOC_GENERATION_PROMPT.format(
            pattern_name=pattern_name.replace("/", " - ").replace("_", " ").title(),
            pattern_id=pattern_name.replace("/", "_"),
            domain=domain,
            subtopic=subtopic,
            count=len(questions),
            years=years_str,
            frequency=frequency,
            sample_questions=sample_text,
            first_year=first_year,
            second_year=second_year,
            third_year=third_year
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"  Error generating doc for {pattern_name}: {e}")
            return self._fallback_doc(pattern_name, questions, stats)
    
    def _select_best_samples(self, questions: List[Dict], n: int = 10) -> List[Dict]:
        """Select best sample questions for examples."""
        # Prioritize:
        # 1. Questions with solutions
        # 2. Recent years
        # 3. Variety of difficulty
        
        with_solutions = [q for q in questions if q.get("solution")]
        without_solutions = [q for q in questions if not q.get("solution")]
        
        # Sort by year (recent first)
        with_solutions.sort(key=lambda x: x.get("year", 0), reverse=True)
        without_solutions.sort(key=lambda x: x.get("year", 0), reverse=True)
        
        # Take from both pools
        samples = with_solutions[:n]
        if len(samples) < n:
            samples.extend(without_solutions[:n - len(samples)])
        
        return samples[:n]
    
    def _format_sample_questions(self, questions: List[Dict]) -> str:
        """Format sample questions for prompt."""
        lines = []
        for i, q in enumerate(questions, 1):
            year = q.get("year", "unknown")
            exam = q.get("exam", "").upper()
            question = q.get("question", "")
            solution = q.get("solution", "No solution provided")
            
            lines.append(f"Q{i} ({exam} {year}):")
            lines.append(f"Question: {question}")
            lines.append(f"Solution: {solution}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _fallback_doc(self, pattern_name: str, questions: List[Dict], stats: Dict) -> str:
        """Generate basic fallback document if LLM fails."""
        parts = pattern_name.split("/")
        domain = parts[0] if len(parts) > 0 else "unknown"
        subtopic = parts[1] if len(parts) > 1 else "unknown"
        
        return f'''---
id: "{pattern_name.replace("/", "_")}"
domain: "{domain}"
subtopic: "{subtopic}"
jee_frequency: "{stats.get("frequency", "unknown") if stats else "unknown"}"
---

# {pattern_name.replace("/", " - ").replace("_", " ").title()}

## Pattern Overview
This pattern covers {len(questions)} questions from JEE.

## Sample Questions
{self._format_sample_questions(questions[:3])}

## Notes
Document generation failed. Please regenerate or edit manually.
'''
    
    async def generate_batch(
        self,
        patterns: Dict[str, List[Dict]],
        stats: Dict[str, Dict],
        output_dir: str,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, str]:
        """
        Generate documents for all patterns.
        
        Args:
            patterns: Dict mapping pattern_key -> questions
            stats: Dict mapping pattern_key -> stats
            output_dir: Directory to save generated docs
            progress_callback: Optional callback(pattern_name, current, total)
        
        Returns:
            Dict mapping pattern_key -> file_path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        total = len(patterns)
        generated = {}
        
        for i, (pattern_name, questions) in enumerate(patterns.items(), 1):
            pattern_stats = stats.get(pattern_name, {})
            
            # Generate document
            doc = await self.generate_doc(pattern_name, questions, pattern_stats)
            
            # Save to file
            file_path = self._save_doc(output_path, pattern_name, doc)
            generated[pattern_name] = str(file_path)
            
            if progress_callback:
                progress_callback(pattern_name, i, total)
            else:
                print(f"  [{i}/{total}] Generated: {pattern_name}")
            
            # Rate limiting
            await asyncio.sleep(self._rate_limit_delay)
        
        return generated
    
    def _save_doc(self, output_dir: Path, pattern_name: str, content: str) -> Path:
        """Save document to file."""
        # Create subdirectory for domain
        parts = pattern_name.split("/")
        domain = parts[0] if len(parts) > 0 else "unknown"
        
        domain_dir = output_dir / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = pattern_name.replace("/", "_") + ".md"
        file_path = domain_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return file_path


if __name__ == "__main__":
    # Test doc generator
    async def test():
        gen = DocGenerator()
        
        test_questions = [
            {
                "year": 2023,
                "exam": "mains",
                "question": "If α, β are roots of x² - 5x + 6 = 0, find α² + β²",
                "solution": "Using Vieta's: α + β = 5, αβ = 6. α² + β² = (α+β)² - 2αβ = 25 - 12 = 13"
            },
            {
                "year": 2022,
                "exam": "advanced",
                "question": "Find the sum of roots of x² - 3x + 2 = 0",
                "solution": "By Vieta's formulas, sum = -(-3)/1 = 3"
            }
        ]
        
        doc = await gen.generate_doc(
            "algebra/quadratic_equations",
            test_questions,
            {"frequency": "very_high"}
        )
        print(doc[:500] + "...")
    
    asyncio.run(test())
