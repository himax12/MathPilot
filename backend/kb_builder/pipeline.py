"""
Main Pipeline Orchestrator for JEE KB Builder.
Coordinates all stages: Load → Classify → Aggregate → Generate → Index
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import sys
import os

# Ensure backend is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from .sources.json_loader import PYQLoader
from .classifier import QuestionClassifier
from .aggregator import PatternAggregator
from .doc_generator import DocGenerator


class JEEKBPipeline:
    """
    Main pipeline orchestrator for JEE Knowledge Base construction.
    
    Pipeline stages:
    1. Load: Read PYQ data from JSON files
    2. Classify: Classify each question by domain/subtopic
    3. Aggregate: Group questions by pattern
    4. Generate: Create KB documents for each pattern
    5. Index: (Optional) Create FAISS embeddings
    """
    
    def __init__(self):
        self.loader = PYQLoader()
        self.classifier = QuestionClassifier()
        self.aggregator = PatternAggregator()
        self.generator = DocGenerator()
        
        # State
        self.questions: List[Dict] = []
        self.patterns: Dict[str, List[Dict]] = {}
        self.stats: Dict[str, Dict] = {}
        self.generated_docs: Dict[str, str] = {}
    
    async def run(
        self, 
        source_path: str, 
        output_dir: str,
        skip_classification: bool = False,
        min_frequency: str = "low"
    ) -> Dict:
        """
        Run the full pipeline.
        
        Args:
            source_path: Path to PYQ data (JSON file or directory)
            output_dir: Directory to save generated KB docs
            skip_classification: Skip if questions are pre-classified
            min_frequency: Minimum frequency to generate docs for
        
        Returns:
            Summary dict with stats
        """
        start_time = datetime.now()
        
        print("=" * 60)
        print("  JEE Knowledge Base Builder Pipeline")
        print("=" * 60)
        
        # Stage 1: Load
        print("\n📥 Stage 1: Loading questions...")
        self.questions = self.loader.load_all(source_path)
        loader_stats = self.loader.get_stats()
        print(f"   Loaded {loader_stats['total']} questions")
        print(f"   Year range: {loader_stats['year_range']}")
        print(f"   With solutions: {loader_stats['with_solutions']}")
        print(f"   Pre-labeled: {loader_stats['pre_labeled']}")
        
        # Stage 2: Classify
        if not skip_classification:
            print("\n🏷️  Stage 2: Classifying questions...")
            await self.classifier.classify_batch(self.questions)
            print(f"   Classification complete!")
        else:
            print("\n🏷️  Stage 2: Skipping classification (pre-classified)")
        
        # Save intermediate results
        self._save_checkpoint(output_dir, "classified_questions.json")
        
        # Stage 3: Aggregate
        print("\n📊 Stage 3: Aggregating patterns...")
        self.patterns = self.aggregator.aggregate(self.questions)
        self.stats = self.aggregator.get_stats()
        print(f"   Found {len(self.patterns)} unique patterns")
        print("\n   Top patterns:")
        for pattern, count in self.aggregator.get_top_patterns(5):
            freq = self.stats[pattern]["frequency"]
            print(f"     {pattern}: {count} questions ({freq})")
        
        # Filter by frequency
        if min_frequency != "low":
            filtered = self.aggregator.filter_by_frequency(min_frequency)
            print(f"\n   Filtered to {len(filtered)} patterns (min: {min_frequency})")
            self.patterns = filtered
        
        # Stage 4: Generate documents
        print("\n📝 Stage 4: Generating KB documents...")
        self.generated_docs = await self.generator.generate_batch(
            self.patterns,
            self.stats,
            output_dir
        )
        print(f"   Generated {len(self.generated_docs)} documents")
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        summary = {
            "questions_loaded": loader_stats['total'],
            "patterns_found": len(self.patterns),
            "documents_generated": len(self.generated_docs),
            "duration_seconds": duration,
            "output_dir": str(output_dir)
        }
        
        print("\n" + "=" * 60)
        print("  ✅ Pipeline Complete!")
        print("=" * 60)
        print(f"\n   Questions: {summary['questions_loaded']}")
        print(f"   Patterns: {summary['patterns_found']}")
        print(f"   Documents: {summary['documents_generated']}")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Output: {output_dir}")
        
        # Save summary
        self._save_summary(output_dir, summary)
        
        return summary
    
    def _save_checkpoint(self, output_dir: str, filename: str):
        """Save intermediate checkpoint."""
        path = Path(output_dir).parent / "checkpoints"
        path.mkdir(parents=True, exist_ok=True)
        
        filepath = path / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)
        
        print(f"   Checkpoint saved: {filepath}")
    
    def _save_summary(self, output_dir: str, summary: Dict):
        """Save pipeline summary."""
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save stats
        stats_path = path / "_stats.json"
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump({
                "summary": summary,
                "pattern_stats": self.stats
            }, f, indent=2)
        
        # Save index
        index_path = path / "_index.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# JEE Math Knowledge Base Index\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(f"Total patterns: {len(self.patterns)}\n\n")
            
            # Group by domain
            by_domain = {}
            for pattern in sorted(self.generated_docs.keys()):
                domain = pattern.split("/")[0]
                if domain not in by_domain:
                    by_domain[domain] = []
                by_domain[domain].append(pattern)
            
            for domain in sorted(by_domain.keys()):
                f.write(f"## {domain.replace('_', ' ').title()}\n\n")
                for pattern in by_domain[domain]:
                    count = len(self.patterns.get(pattern, []))
                    freq = self.stats.get(pattern, {}).get("frequency", "unknown")
                    f.write(f"- [{pattern}]({pattern.replace('/', '_')}.md) ({count} Qs, {freq})\n")
                f.write("\n")


async def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="JEE KB Builder Pipeline")
    parser.add_argument("source", help="Path to PYQ data (JSON file or directory)")
    parser.add_argument("--output", "-o", default="backend/knowledge/base/patterns",
                       help="Output directory for KB docs")
    parser.add_argument("--skip-classification", action="store_true",
                       help="Skip classification if questions are pre-classified")
    parser.add_argument("--min-frequency", choices=["low", "medium", "high", "very_high"],
                       default="low", help="Minimum frequency to generate docs")
    
    args = parser.parse_args()
    
    pipeline = JEEKBPipeline()
    await pipeline.run(
        source_path=args.source,
        output_dir=args.output,
        skip_classification=args.skip_classification,
        min_frequency=args.min_frequency
    )


if __name__ == "__main__":
    asyncio.run(main())
