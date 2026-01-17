"""
Extract Math-only questions from JEE datasets.
Combines JEE Mains (14k+) and JEE Advanced (JEEBench) into unified format.
"""

import json
import re
from pathlib import Path
from typing import List, Dict


def extract_jeebench_math(jeebench_path: str) -> List[Dict]:
    """
    Extract Math questions from JEEBench dataset.
    JEEBench has JEE Advanced 2016-2023 questions.
    """
    dataset_file = Path(jeebench_path) / "extracted" / "data" / "dataset.json"
    
    with open(dataset_file, encoding='utf-8') as f:
        all_questions = json.load(f)
    
    math_questions = []
    
    for q in all_questions:
        # Filter for math only
        if q.get("subject") != "math":
            continue
        
        # Extract year from description (e.g., "JEE Adv 2016 Paper 1")
        desc = q.get("description", "")
        year_match = re.search(r'(\d{4})', desc)
        year = int(year_match.group(1)) if year_match else 0
        
        # Determine paper
        paper = "paper1" if "Paper 1" in desc else "paper2" if "Paper 2" in desc else ""
        
        # Normalize to our format
        math_questions.append({
            "id": f"ADV_{year}_{paper}_{q.get('index', 0)}",
            "year": year,
            "exam": "advanced",
            "shift": paper,
            "question": q.get("question", ""),
            "options": [],  # Options embedded in question text
            "answer": q.get("gold", ""),
            "solution": "",  # JEEBench doesn't have solutions
            "topic": "",  # Will be classified later
            "type": q.get("type", "MCQ"),
            "source": "jeebench"
        })
    
    print(f"Extracted {len(math_questions)} Math questions from JEEBench (JEE Advanced)")
    return math_questions


def extract_jee_mains_math(mains_path: str) -> List[Dict]:
    """
    Extract Math questions from JEE Mains database.
    Uses the jee_data_base package API.
    """
    # The jee_mains_repo uses a package structure
    # We need to check how to access the data
    
    # For now, we'll create a placeholder since the data
    # is accessed via their Python API, not direct JSON
    print("Note: JEE Mains data requires using their package API.")
    print("You can access it via: pip install jee_data_base")
    print("Then use: from jee_data_base import DataBase")
    
    return []


def save_math_questions(questions: List[Dict], output_path: str):
    """Save extracted Math questions to JSON."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(questions)} questions to {output_path}")


def main():
    """Main extraction routine."""
    base_dir = Path(__file__).parent.parent / "data"
    
    all_math_questions = []
    
    # Extract JEE Advanced from JEEBench
    jeebench_path = base_dir / "jeebench_repo"
    if jeebench_path.exists():
        advanced_qs = extract_jeebench_math(str(jeebench_path))
        all_math_questions.extend(advanced_qs)
    else:
        print(f"JEEBench not found at {jeebench_path}")
    
    # Print stats
    print(f"\n=== Extraction Complete ===")
    print(f"Total Math questions: {len(all_math_questions)}")
    
    if all_math_questions:
        years = sorted(set(q["year"] for q in all_math_questions))
        print(f"Year range: {min(years)} - {max(years)}")
        
        by_exam = {}
        for q in all_math_questions:
            exam = q["exam"]
            by_exam[exam] = by_exam.get(exam, 0) + 1
        print(f"By exam: {by_exam}")
    
    # Save combined dataset
    output_path = base_dir / "pyqs" / "jee_math_all.json"
    save_math_questions(all_math_questions, str(output_path))
    
    # Also save a sample for testing
    sample_path = base_dir / "pyqs" / "jee_math_sample.json"
    save_math_questions(all_math_questions[:50], str(sample_path))
    
    return all_math_questions


if __name__ == "__main__":
    main()
