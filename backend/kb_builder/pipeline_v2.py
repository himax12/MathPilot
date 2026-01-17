"""
Quota-Efficient KB Builder Pipeline V2

Key Optimization: The JEE Mains data already has topic/chapter labels!
No need to call LLM for classification - saving 4700+ API calls.

Pipeline:
1. Load pre-labeled questions from JSON
2. Aggregate by existing topic/chapter labels (NO API calls)
3. Generate KB docs using LLM only for aggregated patterns (~50-100 calls)

This reduces API calls from ~4800 to ~100!
"""

import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

try:
    from google import genai
    from google.genai import types
    from backend.config import Config
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def load_questions(input_path: str) -> List[Dict]:
    """Load questions from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def aggregate_by_labels(questions: List[Dict]) -> Dict[str, Dict]:
    """
    Aggregate questions by their EXISTING topic/chapter labels.
    No LLM calls needed - the data is pre-labeled!
    
    Returns:
        Dict mapping "chapter/topic" -> {questions, stats}
    """
    patterns = {}
    
    for q in questions:
        chapter = q.get('chapter', '').strip() or 'unknown'
        topic = q.get('topic', '').strip() or 'general'
        
        # Create pattern key
        pattern_key = f"{chapter}/{topic}"
        
        if pattern_key not in patterns:
            patterns[pattern_key] = {
                "chapter": chapter,
                "topic": topic,
                "questions": [],
                "years": set(),
                "difficulties": {},
                "question_types": {},
                "has_solutions": 0,
                "exams": set()
            }
        
        p = patterns[pattern_key]
        p["questions"].append(q)
        
        # Track stats
        if q.get('year'):
            p["years"].add(q['year'])
        
        diff = q.get('difficulty', 'medium')
        p["difficulties"][diff] = p["difficulties"].get(diff, 0) + 1
        
        qtype = q.get('type', 'mcq')
        p["question_types"][qtype] = p["question_types"].get(qtype, 0) + 1
        
        if q.get('solution'):
            p["has_solutions"] += 1
        
        if q.get('exam'):
            p["exams"].add(q['exam'])
    
    # Convert sets to lists for JSON serialization
    for key, p in patterns.items():
        p["years"] = sorted(p["years"])
        p["count"] = len(p["questions"])
        p["exams"] = list(p["exams"])
        p["jee_frequency"] = len(p["years"])
        
        # Determine primary difficulty
        if p["difficulties"]:
            p["primary_difficulty"] = max(p["difficulties"], key=p["difficulties"].get)
        else:
            p["primary_difficulty"] = "medium"
    
    return patterns


def generate_kb_doc_content(pattern: Dict, max_examples: int = 5) -> str:
    """
    Generate KB document content without LLM.
    Uses the existing solutions from questions as examples.
    """
    chapter = pattern["chapter"].replace("-", " ").title()
    topic = pattern["topic"].replace("-", " ").title()
    
    # Select representative questions with solutions
    examples = [q for q in pattern["questions"] if q.get("solution")][:max_examples]
    
    # Build markdown content
    lines = [
        f"---",
        f"chapter: {pattern['chapter']}",
        f"topic: {pattern['topic']}",
        f"jee_frequency: {pattern['jee_frequency']}",
        f"years_appeared: {pattern['years']}",
        f"question_count: {pattern['count']}",
        f"difficulty: {pattern['primary_difficulty']}",
        f"question_types: {list(pattern['question_types'].keys())}",
        f"exams: {pattern['exams']}",
        f"---",
        f"",
        f"# {chapter}: {topic}",
        f"",
        f"**JEE Frequency**: Appeared in **{pattern['jee_frequency']} years** ({min(pattern['years']) if pattern['years'] else 'N/A'} - {max(pattern['years']) if pattern['years'] else 'N/A'})",
        f"",
        f"**Question Count**: {pattern['count']} questions",
        f"",
        f"## Question Types",
        f"",
    ]
    
    for qtype, count in pattern['question_types'].items():
        lines.append(f"- **{qtype.upper()}**: {count} questions")
    
    lines.extend([
        f"",
        f"## Difficulty Distribution",
        f"",
    ])
    
    for diff, count in pattern['difficulties'].items():
        lines.append(f"- **{diff.title()}**: {count} questions")
    
    if examples:
        lines.extend([
            f"",
            f"## Worked Examples",
            f"",
        ])
        
        for i, ex in enumerate(examples, 1):
            lines.extend([
                f"### Example {i} (Year: {ex.get('year', 'N/A')})",
                f"",
                f"**Question:**",
                f"",
                f"{ex.get('question', 'N/A')[:500]}{'...' if len(ex.get('question', '')) > 500 else ''}",
                f"",
                f"**Solution:**",
                f"",
                f"{ex.get('solution', 'No solution available')[:1000]}{'...' if len(ex.get('solution', '')) > 1000 else ''}",
                f"",
            ])
    
    return "\n".join(lines)


async def generate_enhanced_kb_doc(pattern: Dict, client, model_name: str) -> str:
    """
    Generate enhanced KB doc using LLM (only for high-frequency patterns).
    This is the ONLY place LLM is used.
    """
    chapter = pattern["chapter"].replace("-", " ").title()
    topic = pattern["topic"].replace("-", " ").title()
    
    # Select sample questions for context
    samples = pattern["questions"][:5]
    sample_text = "\n\n".join([
        f"Q{i+1}: {q.get('question', '')[:300]}" 
        for i, q in enumerate(samples)
    ])
    
    prompt = f"""You are a JEE Math expert. Create a concise knowledge base document for:

Chapter: {chapter}
Topic: {topic}
JEE Frequency: {pattern['jee_frequency']} years
Question Count: {pattern['count']} questions

Sample Questions:
{sample_text}

Generate a document with:
1. **Pattern Recognition** (2-3 bullet points): How to identify this pattern
2. **Core Formulas** (3-5 key formulas in LaTeX)
3. **Standard Approach** (numbered steps, max 5)
4. **Quick Tips** (2-3 exam tricks)
5. **Common Mistakes** (2-3 pitfalls to avoid)

Be concise. Focus on JEE-specific patterns. Use LaTeX for math."""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        llm_content = response.text
    except Exception as e:
        print(f"  LLM error for {chapter}/{topic}: {e}")
        llm_content = "LLM generation failed - using basic template."
    
    # Combine with metadata
    header = f"""---
chapter: {pattern['chapter']}
topic: {pattern['topic']}
jee_frequency: {pattern['jee_frequency']}
years_appeared: {pattern['years']}
question_count: {pattern['count']}
difficulty: {pattern['primary_difficulty']}
---

# {chapter}: {topic}

**JEE Frequency**: {pattern['jee_frequency']} years | **Questions**: {pattern['count']}

"""
    
    return header + llm_content


async def run_pipeline(
    input_path: str,
    output_dir: str,
    use_llm: bool = False,
    llm_threshold: int = 5,  # Only use LLM for patterns with >= this many questions
    batch_size: int = 5,
    delay_between_batches: float = 2.0
):
    """
    Run the quota-efficient KB builder pipeline.
    
    Args:
        input_path: Path to questions JSON
        output_dir: Output directory for KB docs
        use_llm: Whether to use LLM for high-frequency patterns
        llm_threshold: Min question count to use LLM
        batch_size: Questions per LLM batch
        delay_between_batches: Seconds between batches (rate limiting)
    """
    print("=" * 60)
    print("  KB Builder Pipeline V2 (Quota-Efficient)")
    print("=" * 60)
    
    # Setup
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Stage 1: Load questions
    print("\n[Stage 1/3] Loading questions...")
    questions = load_questions(input_path)
    print(f"  Loaded {len(questions)} questions")
    
    # Stage 2: Aggregate by existing labels (NO API CALLS!)
    print("\n[Stage 2/3] Aggregating by existing labels (NO API calls!)...")
    patterns = aggregate_by_labels(questions)
    print(f"  Found {len(patterns)} unique patterns")
    
    # Show top patterns
    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]['count'], reverse=True)
    print(f"\n  Top 10 patterns by question count:")
    for key, p in sorted_patterns[:10]:
        print(f"    - {key}: {p['count']} questions, {p['jee_frequency']} years")
    
    # Stage 3: Generate KB docs
    print("\n[Stage 3/3] Generating KB documents...")
    
    if use_llm and GEMINI_AVAILABLE:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        model_name = "gemini-2.0-flash"
        
        # Only use LLM for high-frequency patterns
        high_freq_patterns = [(k, p) for k, p in sorted_patterns if p['count'] >= llm_threshold]
        low_freq_patterns = [(k, p) for k, p in sorted_patterns if p['count'] < llm_threshold]
        
        print(f"  Using LLM for {len(high_freq_patterns)} high-frequency patterns (>= {llm_threshold} questions)")
        print(f"  Using templates for {len(low_freq_patterns)} low-frequency patterns")
        
        # Process high-frequency patterns with LLM in batches
        llm_count = 0
        for i in range(0, len(high_freq_patterns), batch_size):
            batch = high_freq_patterns[i:i+batch_size]
            
            for key, pattern in batch:
                try:
                    content = await generate_enhanced_kb_doc(pattern, client, model_name)
                    llm_count += 1
                except Exception as e:
                    print(f"  Error with LLM for {key}: {e}")
                    content = generate_kb_doc_content(pattern)
                
                # Save document
                safe_name = key.replace("/", "_").replace(" ", "_")
                doc_path = output_path / f"{safe_name}.md"
                doc_path.write_text(content, encoding='utf-8')
            
            # Rate limiting
            if i + batch_size < len(high_freq_patterns):
                print(f"  Processed {min(i+batch_size, len(high_freq_patterns))}/{len(high_freq_patterns)} high-freq patterns...")
                await asyncio.sleep(delay_between_batches)
        
        print(f"  LLM calls made: {llm_count}")
        
        # Process low-frequency patterns with templates (NO API calls)
        for key, pattern in low_freq_patterns:
            content = generate_kb_doc_content(pattern)
            safe_name = key.replace("/", "_").replace(" ", "_")
            doc_path = output_path / f"{safe_name}.md"
            doc_path.write_text(content, encoding='utf-8')
    
    else:
        # No LLM - use templates for all (ZERO API calls!)
        print("  Using templates for all patterns (ZERO API calls)")
        for key, pattern in sorted_patterns:
            content = generate_kb_doc_content(pattern)
            safe_name = key.replace("/", "_").replace(" ", "_")
            doc_path = output_path / f"{safe_name}.md"
            doc_path.write_text(content, encoding='utf-8')
    
    # Generate index
    index_lines = [
        "# JEE Math Knowledge Base Index",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Total Patterns: {len(patterns)}",
        f"Total Questions: {len(questions)}",
        "",
        "## Patterns by Frequency",
        "",
        "| Chapter | Topic | Questions | Years |",
        "|---------|-------|-----------|-------|",
    ]
    
    for key, p in sorted_patterns[:50]:  # Top 50
        index_lines.append(
            f"| {p['chapter']} | {p['topic']} | {p['count']} | {p['jee_frequency']} |"
        )
    
    index_path = output_path / "_index.md"
    index_path.write_text("\n".join(index_lines), encoding='utf-8')
    
    print(f"\n✅ Pipeline complete!")
    print(f"   Output directory: {output_path}")
    print(f"   Total documents: {len(patterns)}")
    print(f"   Index: {index_path}")
    
    return {
        "patterns": len(patterns),
        "questions": len(questions),
        "output_dir": str(output_path)
    }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quota-Efficient KB Builder v2")
    parser.add_argument("input", help="Path to questions JSON")
    parser.add_argument("--output", "-o", default="backend/knowledge/base/patterns", 
                        help="Output directory")
    parser.add_argument("--use-llm", action="store_true",
                        help="Use LLM for high-frequency patterns")
    parser.add_argument("--llm-threshold", type=int, default=10,
                        help="Min questions to use LLM (default: 10)")
    parser.add_argument("--batch-size", type=int, default=5,
                        help="LLM batch size (default: 5)")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Delay between batches in seconds (default: 2.0)")
    
    args = parser.parse_args()
    
    asyncio.run(run_pipeline(
        input_path=args.input,
        output_dir=args.output,
        use_llm=args.use_llm,
        llm_threshold=args.llm_threshold,
        batch_size=args.batch_size,
        delay_between_batches=args.delay
    ))


if __name__ == "__main__":
    main()
