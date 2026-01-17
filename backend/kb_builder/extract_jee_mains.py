"""
Extract Math questions from JEE Mains database (jee_data_base package).
This uses the installed jee_data_base package API.
"""

import json
from pathlib import Path
from typing import List, Dict

try:
    from jee_data_base import DataBase
    from jee_data_base.core.filter import Filter
    JEE_DB_AVAILABLE = True
except ImportError:
    JEE_DB_AVAILABLE = False
    print("jee_data_base not installed. Run: pip install jee_data_base")


def extract_jee_mains_math() -> List[Dict]:
    """
    Extract all Mathematics questions from JEE Mains database.
    
    Returns:
        List of normalized question dicts
    """
    if not JEE_DB_AVAILABLE:
        return []
    
    print("Initializing JEE Mains database...")
    db = DataBase()
    print(f"Database loaded: {db.name}")
    print(f"Total chapters: {len(db.chapters_dict)}")
    print(f"State: {db.state}")
    
    # Create filter
    f = Filter(db.chapters_dict)
    
    # Get all Math questions
    print("\nFiltering for Mathematics questions...")
    math_questions = f.by_subject("mathematics").get()
    print(f"Total Math questions: {len(math_questions)}")
    
    # Normalize to our format
    normalized = []
    for q in math_questions:
        try:
            # Build options list
            options = []
            if q.options:
                for opt in q.options:
                    if isinstance(opt, dict):
                        options.append(opt.get("content", ""))
                    else:
                        options.append(str(opt))
            
            normalized.append({
                "id": f"MAINS_{q.year}_{q.question_id}",
                "year": q.year if q.year else 0,
                "exam": "mains",
                "shift": q.paperTitle or "",
                "question": q.question or "",
                "options": options,
                "answer": q.answer or "",
                "solution": q.explanation or "",
                "topic": q.topic or "",
                "chapter": q.chapter or "",
                "difficulty": q.difficulty or "",
                "type": q.type or "MCQ",
                "source": "jee_data_base"
            })
        except Exception as e:
            print(f"  Error processing question: {e}")
            continue
    
    return normalized


def get_stats(questions: List[Dict]) -> Dict:
    """Get statistics about extracted questions."""
    if not questions:
        return {"total": 0}
    
    years = [q["year"] for q in questions if q["year"]]
    chapters = [q["chapter"] for q in questions if q["chapter"]]
    topics = [q["topic"] for q in questions if q["topic"]]
    with_solutions = sum(1 for q in questions if q["solution"])
    
    return {
        "total": len(questions),
        "year_range": (min(years), max(years)) if years else (0, 0),
        "with_solutions": with_solutions,
        "unique_chapters": len(set(chapters)),
        "unique_topics": len(set(topics)),
        "years_distribution": {y: years.count(y) for y in sorted(set(years))}
    }


def main():
    """Main extraction routine."""
    print("=" * 60)
    print("  JEE Mains Math Extractor")
    print("=" * 60)
    
    # Extract
    questions = extract_jee_mains_math()
    
    if not questions:
        print("No questions extracted. Check if jee_data_base is installed.")
        return
    
    # Get stats
    stats = get_stats(questions)
    print(f"\n=== Extraction Stats ===")
    print(f"Total questions: {stats['total']}")
    print(f"Year range: {stats['year_range']}")
    print(f"With solutions: {stats['with_solutions']}")
    print(f"Unique chapters: {stats['unique_chapters']}")
    print(f"Unique topics: {stats['unique_topics']}")
    
    # Save
    output_dir = Path(__file__).parent.parent / "data" / "pyqs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "jee_mains_math.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to: {output_file}")
    
    # Save sample
    sample_file = output_dir / "jee_mains_math_sample.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(questions[:100], f, indent=2, ensure_ascii=False)
    print(f"Sample saved to: {sample_file}")
    
    return questions


if __name__ == "__main__":
    main()
