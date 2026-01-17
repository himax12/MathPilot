"""
Schemas - Data contracts for all Math Mentor components.
Single source of truth for data structures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime


@dataclass
class InputData:
    """Raw input from any modality."""
    type: Literal["text", "image", "audio"]
    raw: Any  # bytes for image/audio, str for text
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedProblem:
    """Output from Parser Agent."""
    problem_text: str
    topic: str  # algebra, calculus, probability, linear_algebra
    variables: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    given: Dict[str, Any] = field(default_factory=dict)
    question: str = ""
    approach: str = ""
    relationships: List[str] = field(default_factory=list)
    needs_clarification: bool = False
    confidence: float = 0.0
    error: Optional[str] = None


@dataclass
class RouteDecision:
    """Output from Router Agent."""
    domain: str  # algebra, calculus, probability, etc.
    subtopic: str  # e.g., quadratic, conditional_probability
    strategy: str  # e.g., quadratic_formula, bayes_theorem
    rag_filters: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class Solution:
    """Output from Solver Agent."""
    code: str
    answer: Any
    reasoning: str = ""
    sources: List[Dict[str, Any]] = field(default_factory=list)  # RAG citations
    error: Optional[str] = None


@dataclass
class Verification:
    """Output from Verifier Agent."""
    is_valid: bool
    confidence: float
    issues: List[str] = field(default_factory=list)
    checks_performed: List[Dict[str, Any]] = field(default_factory=list)
    needs_hitl: bool = False
    error: Optional[str] = None


@dataclass
class Explanation:
    """Output from Explainer Agent."""
    intuition: str = ""
    steps: List[Dict[str, str]] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class Feedback:
    """User feedback on a solution."""
    rating: Literal["correct", "incorrect", "partial"]
    comment: Optional[str] = None
    corrections: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryRecord:
    """Complete record for persistent storage."""
    id: str
    timestamp: datetime
    input_data: InputData
    parsed: ParsedProblem
    route: Optional[RouteDecision] = None
    solution: Optional[Solution] = None
    verification: Optional[Verification] = None
    explanation: Optional[Explanation] = None
    feedback: Optional[Feedback] = None
