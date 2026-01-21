"""
Question Classifier for JEE KB Builder.
Uses Gemini to classify questions by domain, subtopic, and pattern.
"""

import json
import asyncio
from typing import Dict, List, Optional

from backend.config import config

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False


class QuestionClassifier:
    """
    Classify JEE questions by domain, subtopic, and pattern type.
    
    Uses the Router Agent taxonomy for consistent classification
    across the knowledge base and runtime routing.
    """
    
    CLASSIFICATION_PROMPT = '''You are a JEE Math question classifier. Classify this question:

Question: {question}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "domain": "<algebra|calculus|coordinate_geometry|vectors_3d|trigonometry|probability>",
  "subtopic": "<specific subtopic from JEE syllabus>",
  "pattern_type": "<formula_application|property_application|problem_solving|proof|conceptual>",
  "difficulty": "<basic|intermediate|advanced>",
  "techniques": ["<technique1>", "<technique2>"],
  "key_concepts": ["<concept1>", "<concept2>"]
}}

Domains and subtopics:
- algebra: quadratic_equations, sequences_series, complex_numbers, permutations_combinations, binomial_theorem, matrices_determinants
- calculus: limits, continuity_differentiability, differentiation, applications_of_derivatives, indefinite_integration, definite_integration, area_under_curves, differential_equations
- coordinate_geometry: straight_lines, circles, parabola, ellipse, hyperbola
- vectors_3d: vector_algebra, 3d_geometry
- trigonometry: identities_equations, inverse_trigonometry, properties_of_triangles
- probability: basic_probability, conditional_probability, distributions
'''

    def __init__(self):
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai not installed. Run: uv add google-genai")
        
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = config.GEMINI_MODEL
        self._request_count = 0
        self._rate_limit_delay = 0.5  # seconds between requests
    
    async def classify(self, question: Dict) -> Dict:
        """
        Classify a single question.
        
        Returns:
            Classification dict with domain, subtopic, pattern_type, etc.
        """
        question_text = question.get("question", "")
        if not question_text:
            return self._empty_classification()
        
        prompt = self.CLASSIFICATION_PROMPT.format(question=question_text)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            text = response.text.strip()
            
            # Clean markdown code blocks if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            
            classification = json.loads(text)
            return classification
            
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
            return self._empty_classification()
        except Exception as e:
            print(f"  Classification error: {e}")
            return self._empty_classification()
    
    async def classify_batch(
        self, 
        questions: List[Dict], 
        batch_size: int = 5,
        progress_callback: Optional[callable] = None
    ) -> List[Dict]:
        """
        Classify questions in batches with rate limiting.
        
        Args:
            questions: List of question dicts
            batch_size: Questions per batch
            progress_callback: Optional callback(processed, total)
        
        Returns:
            Same list with 'classification' field populated
        """
        total = len(questions)
        processed = 0
        
        for i in range(0, total, batch_size):
            batch = questions[i:i+batch_size]
            
            for q in batch:
                # Skip if already classified
                if q.get("classification"):
                    processed += 1
                    continue
                
                q["classification"] = await self.classify(q)
                processed += 1
                
                # Rate limiting
                await asyncio.sleep(self._rate_limit_delay)
            
            if progress_callback:
                progress_callback(processed, total)
            else:
                print(f"  Classified {processed}/{total} questions...")
        
        return questions
    
    def _empty_classification(self) -> Dict:
        """Return empty classification for failed cases."""
        return {
            "domain": "unknown",
            "subtopic": "unknown",
            "pattern_type": "unknown",
            "difficulty": "unknown",
            "techniques": [],
            "key_concepts": []
        }


if __name__ == "__main__":
    # Test classifier
    async def test():
        classifier = QuestionClassifier()
        
        test_question = {
            "question": "If α, β are roots of x² - 5x + 6 = 0, find α² + β²"
        }
        
        result = await classifier.classify(test_question)
        print(f"Classification: {json.dumps(result, indent=2)}")
    
    asyncio.run(test())
