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
            
    def retrieve(self, query: str, top_k: int = 3, filters: List[str] = None) -> str:
        """
        Retrieve relevant knowledge and format it as a context string for the LLM.
        
        Args:
            query: The user's math problem or question.
            top_k: Number of documents to retrieve.
            filters: Optional list of domain/topic filters (from Router).
            
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
            
            context_parts = ["**RELEVANT KNOWLEDGE BASE ENTRIES:**"]
            
            for i, res in enumerate(results, 1):
                doc_id = res['doc_id']
                # Fetch full content
                content = self.embedder.get_document_content(doc_id)
                
                if content:
                    # Create a concise header
                    header = f"--- Source {i}: {res['chapter']} > {res['topic']} (Frequency: {res['jee_frequency']}) ---"
                    context_parts.append(f"{header}\n{content.strip()}\n")
                    
            if len(context_parts) == 1:
                return ""
                
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")
            return ""
