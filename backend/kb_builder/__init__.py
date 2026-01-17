"""
JEE KB Builder - Automated Knowledge Base Construction Pipeline

Processes JEE Mains + Advanced PYQs (20 years) to generate
a comprehensive pattern-based knowledge base for RAG retrieval.
"""

from .pipeline import JEEKBPipeline

__all__ = ["JEEKBPipeline"]
