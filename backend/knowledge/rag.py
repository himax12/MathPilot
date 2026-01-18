"""
MathRAG - Runtime wrapper for Knowledge Base retrieval.
Adapts the build-time KBEmbedder for use in the runtime SolverAgent.
"""

import sys
import os
from typing import List, Dict, Any, Optional

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

try:
    from kb_builder.embedder import KBEmbedder
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: Could not import KBEmbedder. RAG will be disabled.")

class MathRAG:
    """
    Retrieval-Augmented Generation engine for Math Mentor.
    Wraps the FAISS-based KBEmbedder.
    """
    
    def __init__(self, index_dir: Optional[str] = None):
        """
        Initialize the RAG engine.
        
        Args:
            index_dir: Override path to index directory. Defaults to backend/knowledge/index.
        """
        self.ready = False
        if not RAG_AVAILABLE:
            return
            
        try:
            self.embedder = KBEmbedder()
            
            # Default to adjacent index directory
            if index_dir is None:
                index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index")
                
            self.embedder.load_index(index_dir)
            self.ready = True
            print(f"✅ MathRAG initialized using index at: {index_dir}")
            
        except Exception as e:
            print(f"⚠️ MathRAG Initialization Failed: {e}")
            self.ready = False
            
    def retrieve(self, query: str, top_k: int = 3, filters: List[str] = None, min_similarity: float = 0.25) -> str:
        """
        Retrieve relevant knowledge and format it as a context string for the LLM.
        
        Args:
            query: The user's math problem or question.
            top_k: Number of documents to retrieve.
            filters: Optional list of domain/topic filters (from Router).
            min_similarity: Minimum similarity score (0-1) to include a result.
            
        Returns:
            Formatted string containing retrieved documents, or empty string if RAG fails.
        """
        if not self.ready:
            return ""
            
        try:
            # Map simple filters to chapter filtering logic if needed (future enhancement)
            # For now, rely on semantic similarity search
            
            results = self.embedder.search(query, top_k=top_k)
            
            if not results:
                return ""
            
            # Filter by minimum similarity threshold
            filtered_results = [r for r in results if r.get('similarity', 0) >= min_similarity]
            
            if not filtered_results:
                print(f"RAG: All {len(results)} results below similarity threshold ({min_similarity})")
                return ""
            
            context_parts = ["**RELEVANT KNOWLEDGE BASE ENTRIES:**"]
            
            for i, res in enumerate(filtered_results, 1):
                doc_id = res['doc_id']
                # Fetch full content
                content = self.embedder.get_document_content(doc_id)
                
                if content:
                    # Create a concise header with similarity score
                    sim_pct = res.get('similarity', 0) * 100
                    header = f"--- Source {i}: {res['chapter']} > {res['topic']} (Relevance: {sim_pct:.0f}%) ---"
                    context_parts.append(f"{header}\n{content.strip()}\n")
                    
            if len(context_parts) == 1:
                return ""
                
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")
            return ""
    
    def retrieve_with_score(self, query: str, top_k: int = 3, min_similarity: float = 0.25) -> Dict[str, Any]:
        """
        Retrieve relevant knowledge WITH similarity score for two-tier solving.
        
        Args:
            query: The user's math problem or question.
            top_k: Number of documents to retrieve.
            min_similarity: Minimum similarity score to include a result.
            
        Returns:
            Dict with:
                - 'context': Formatted string of retrieved documents
                - 'max_similarity': Highest similarity score (0-1)
                - 'has_strong_match': True if max_similarity >= 0.6
                - 'top_topic': The topic of the best match
        """
        if not self.ready:
            return {"context": "", "max_similarity": 0.0, "has_strong_match": False, "top_topic": ""}
            
        try:
            results = self.embedder.search(query, top_k=top_k)
            
            if not results:
                return {"context": "", "max_similarity": 0.0, "has_strong_match": False, "top_topic": ""}
            
            # Get max similarity
            max_sim = max(r.get('similarity', 0) for r in results)
            top_result = max(results, key=lambda r: r.get('similarity', 0))
            top_topic = f"{top_result.get('chapter', '')} > {top_result.get('topic', '')}"
            
            # Filter by minimum similarity threshold
            filtered_results = [r for r in results if r.get('similarity', 0) >= min_similarity]
            
            if not filtered_results:
                return {"context": "", "max_similarity": max_sim, "has_strong_match": False, "top_topic": top_topic}
            
            context_parts = ["**RELEVANT KNOWLEDGE BASE ENTRIES:**"]
            
            for i, res in enumerate(filtered_results, 1):
                doc_id = res['doc_id']
                content = self.embedder.get_document_content(doc_id)
                
                if content:
                    sim_pct = res.get('similarity', 0) * 100
                    header = f"--- Source {i}: {res['chapter']} > {res['topic']} (Relevance: {sim_pct:.0f}%) ---"
                    context_parts.append(f"{header}\n{content.strip()}\n")
            
            context = "\n\n".join(context_parts) if len(context_parts) > 1 else ""
            
            return {
                "context": context,
                "max_similarity": max_sim,
                "has_strong_match": max_sim >= 0.6,
                "top_topic": top_topic
            }
            
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")
            return {"context": "", "max_similarity": 0.0, "has_strong_match": False, "top_topic": ""}
