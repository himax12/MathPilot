"""
JSON Loader for JEE PYQ Data.
Loads questions from structured JSON files.
"""

from typing import List, Dict, Optional
from pathlib import Path
import json
import glob


class PYQLoader:
    """
    Load JEE PYQs from various formats.
    
    Supports:
    - Single JSON file with all questions
    - Directory of JSON files (one per year/shift)
    - Pre-labeled or unlabeled questions
    """
    
    def __init__(self):
        self.questions: List[Dict] = []
    
    def load_from_json(self, file_path: str) -> List[Dict]:
        """
        Load questions from a single JSON file.
        
        Expected format:
        [
            {
                "id": "2023_M_S1_Q1",
                "year": 2023,
                "exam": "mains",
                "shift": "shift1",
                "question": "If α, β are roots of x² - 5x + 6 = 0...",
                "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
                "answer": "B",
                "solution": "Using Vieta's formulas...",
                "topic": "quadratic_equations"
            }
        ]
        """
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        
        questions = []
        for idx, q in enumerate(data):
            questions.append(self._normalize_question(q, idx))
        
        return questions
    
    def load_from_directory(self, dir_path: str) -> List[Dict]:
        """Load all JSON files from a directory."""
        all_questions = []
        
        json_files = glob.glob(f"{dir_path}/**/*.json", recursive=True)
        
        for file_path in json_files:
            try:
                file_questions = self.load_from_json(file_path)
                all_questions.extend(file_questions)
                print(f"  Loaded {len(file_questions)} from {Path(file_path).name}")
            except Exception as e:
                print(f"  Error loading {file_path}: {e}")
        
        return all_questions
    
    def load_all(self, source_path: str) -> List[Dict]:
        """
        Load questions from file or directory.
        Auto-detects based on path.
        """
        path = Path(source_path)
        
        if path.is_file():
            self.questions = self.load_from_json(source_path)
        elif path.is_dir():
            self.questions = self.load_from_directory(source_path)
        else:
            raise ValueError(f"Path not found: {source_path}")
        
        return self.questions
    
    def _normalize_question(self, q: Dict, idx: int) -> Dict:
        """Normalize question format for consistency."""
        return {
            "id": q.get("id") or f"Q_{idx}",
            "year": q.get("year") or self._extract_year(q),
            "exam": q.get("exam") or q.get("type") or "unknown",
            "shift": q.get("shift") or q.get("session") or "",
            "question": q.get("question") or q.get("text") or q.get("problem") or "",
            "options": q.get("options") or q.get("choices") or [],
            "answer": q.get("answer") or q.get("correct_answer") or "",
            "solution": q.get("solution") or q.get("explanation") or "",
            "topic": q.get("topic") or q.get("chapter") or "",
            "subtopic": q.get("subtopic") or "",
            # Classification will be filled later
            "classification": q.get("classification") or None
        }
    
    def _extract_year(self, q: Dict) -> int:
        """Try to extract year from question data."""
        # Check common fields
        for field in ["year", "Year", "paper_year", "date"]:
            if field in q:
                try:
                    return int(str(q[field])[:4])
                except:
                    pass
        return 0
    
    def get_stats(self) -> Dict:
        """Get statistics about loaded questions."""
        if not self.questions:
            return {"total": 0}
        
        years = [q["year"] for q in self.questions if q["year"]]
        exams = [q["exam"] for q in self.questions]
        topics = [q["topic"] for q in self.questions if q["topic"]]
        
        return {
            "total": len(self.questions),
            "year_range": (min(years), max(years)) if years else (0, 0),
            "exams": {"mains": exams.count("mains"), "advanced": exams.count("advanced")},
            "with_solutions": sum(1 for q in self.questions if q["solution"]),
            "pre_labeled": sum(1 for q in self.questions if q["topic"]),
            "unique_topics": len(set(topics))
        }


if __name__ == "__main__":
    # Test loader
    loader = PYQLoader()
    
    # Example: Load from test path
    test_path = "backend/data/pyqs"
    try:
        questions = loader.load_all(test_path)
        print(f"\nLoaded {len(questions)} questions")
        print(f"Stats: {loader.get_stats()}")
    except Exception as e:
        print(f"Error: {e}")
        print("Create test data at backend/data/pyqs/ to test")
