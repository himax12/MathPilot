"""
Combine JEE Mains and Advanced Math datasets into unified file.
"""

import json
from pathlib import Path


def main():
    pyqs_dir = Path("backend/data/pyqs")
    
    # Load JEE Mains Math
    with open(pyqs_dir / "jee_mains_math.json", 'r', encoding='utf-8') as f:
        mains = json.load(f)
    print(f"JEE Mains Math: {len(mains)} questions")
    
    # Load JEE Advanced Math
    with open(pyqs_dir / "jee_math_all.json", 'r', encoding='utf-8') as f:
        advanced = json.load(f)
    print(f"JEE Advanced Math: {len(advanced)} questions")
    
    # Combine
    combined = mains + advanced
    print(f"Total: {len(combined)} questions")
    
    # Get stats
    years = sorted(set(q['year'] for q in combined if q.get('year')))
    print(f"Years: {years[0]}-{years[-1]}")
    
    mains_count = sum(1 for q in combined if q.get('exam') == 'mains')
    adv_count = sum(1 for q in combined if q.get('exam') == 'advanced')
    print(f"Mains: {mains_count}, Advanced: {adv_count}")
    
    with_solutions = sum(1 for q in combined if q.get('solution'))
    print(f"With solutions: {with_solutions}")
    
    # Save combined
    output_file = pyqs_dir / "jee_math_complete.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
