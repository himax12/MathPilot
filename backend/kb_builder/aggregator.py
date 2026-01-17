"""
Pattern Aggregator for JEE KB Builder.
Groups classified questions by pattern for document generation.
"""

from collections import defaultdict
from typing import List, Dict, Tuple


class PatternAggregator:
    """
    Group questions by pattern for KB generation.
    
    Creates pattern groups like:
    - calculus/definite_integration
    - algebra/quadratic_equations
    - coordinate_geometry/parabola
    """
    
    def __init__(self):
        self.patterns: Dict[str, List[Dict]] = {}
        self.stats: Dict[str, Dict] = {}
    
    def aggregate(self, questions: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group questions by domain/subtopic.
        
        Returns:
            Dict mapping pattern_key -> list of questions
        """
        patterns = defaultdict(list)
        
        for q in questions:
            cls = q.get("classification", {})
            domain = cls.get("domain", "unknown")
            subtopic = cls.get("subtopic", "unknown")
            
            # Create pattern key
            key = f"{domain}/{subtopic}"
            patterns[key].append(q)
        
        self.patterns = dict(patterns)
        return self.patterns
    
    def aggregate_by_technique(self, questions: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Alternative grouping by technique used.
        Useful for method-specific KB docs.
        """
        patterns = defaultdict(list)
        
        for q in questions:
            cls = q.get("classification", {})
            techniques = cls.get("techniques", [])
            
            for technique in techniques:
                key = f"techniques/{technique}"
                patterns[key].append(q)
        
        return dict(patterns)
    
    def get_stats(self, patterns: Dict[str, List[Dict]] = None) -> Dict[str, Dict]:
        """
        Get statistics for each pattern.
        
        Returns:
            Dict mapping pattern_key -> stats dict
        """
        if patterns is None:
            patterns = self.patterns
        
        stats = {}
        
        for pattern_key, questions in patterns.items():
            years = [q.get("year", 0) for q in questions if q.get("year")]
            exams = [q.get("exam", "") for q in questions]
            difficulties = [
                q.get("classification", {}).get("difficulty", "unknown")
                for q in questions
            ]
            
            stats[pattern_key] = {
                "count": len(questions),
                "years": sorted(set(years)) if years else [],
                "year_range": (min(years), max(years)) if years else (0, 0),
                "frequency": self._compute_frequency(len(questions)),
                "exams": {
                    "mains": exams.count("mains"),
                    "advanced": exams.count("advanced")
                },
                "difficulty_distribution": {
                    "basic": difficulties.count("basic"),
                    "intermediate": difficulties.count("intermediate"),
                    "advanced": difficulties.count("advanced")
                },
                "with_solutions": sum(1 for q in questions if q.get("solution"))
            }
        
        self.stats = stats
        return stats
    
    def _compute_frequency(self, count: int) -> str:
        """Compute frequency category based on count."""
        if count > 50:
            return "very_high"
        elif count > 20:
            return "high"
        elif count > 10:
            return "medium"
        else:
            return "low"
    
    def get_top_patterns(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top N patterns by question count."""
        sorted_patterns = sorted(
            self.patterns.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        return [(k, len(v)) for k, v in sorted_patterns[:n]]
    
    def filter_by_frequency(self, min_frequency: str = "medium") -> Dict[str, List[Dict]]:
        """
        Filter patterns by minimum frequency.
        
        Args:
            min_frequency: 'low', 'medium', 'high', or 'very_high'
        """
        frequency_order = ["low", "medium", "high", "very_high"]
        min_idx = frequency_order.index(min_frequency)
        
        if not self.stats:
            self.get_stats()
        
        filtered = {}
        for pattern_key, questions in self.patterns.items():
            pattern_freq = self.stats.get(pattern_key, {}).get("frequency", "low")
            if frequency_order.index(pattern_freq) >= min_idx:
                filtered[pattern_key] = questions
        
        return filtered
    
    def summary(self) -> str:
        """Get human-readable summary."""
        if not self.patterns:
            return "No patterns aggregated yet."
        
        lines = [
            f"Total patterns: {len(self.patterns)}",
            f"Total questions: {sum(len(qs) for qs in self.patterns.values())}",
            "",
            "Top 10 patterns:"
        ]
        
        for pattern, count in self.get_top_patterns(10):
            lines.append(f"  {pattern}: {count} questions")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Test aggregator
    test_questions = [
        {"classification": {"domain": "calculus", "subtopic": "integration"}, "year": 2023},
        {"classification": {"domain": "calculus", "subtopic": "integration"}, "year": 2022},
        {"classification": {"domain": "algebra", "subtopic": "quadratics"}, "year": 2023},
    ]
    
    agg = PatternAggregator()
    patterns = agg.aggregate(test_questions)
    stats = agg.get_stats()
    
    print(agg.summary())
