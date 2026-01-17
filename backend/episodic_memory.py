"""
Episodic Memory - FAISS-based semantic search for conversation history.
Inherits from KBEmbedder to reuse Gemini embedding logic and FAISS management.
"""

import sys
import os
from typing import Dict, Any, List

# Ensure backend definitions are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from kb_builder.embedder import KBEmbedder
    import faiss
    import numpy as np
except ImportError:
    KBEmbedder = object # Dummy
    print("Warning: Dependencies missing for EpisodicMemory")

class EpisodicMemory(KBEmbedder):
    """
    Dynamic memory system for storing and retrieving past user interactions.
    Persists to 'memory_index' directory.
    """
    
    def __init__(self, index_dir: str = "memory_index"):
        """Initialize Episodic Memory."""
        # Initialize parent (sets up Gemini client)
        super().__init__()
        
        self.index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), index_dir)
        self.dimension = self.EMBEDDING_DIMENSION
        
        # Try to load existing index, or create new
        try:
            self.load_index(self.index_dir)
            print(f"✅ Loaded episodic memory with {self.index.ntotal} vectors")
        except (FileNotFoundError, ValueError):
            print("🆕 Initializing new episodic memory index")
            self._init_empty_index()
            
    def _init_empty_index(self):
        """Create a fresh FAISS index."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        
    def add_interaction(self, role: str, content: str, session_id: str):
        """
        Add a single interaction (User or Assistant message) to memory.
        
        Args:
            role: "user" or "assistant"
            content: The text content
            session_id: Current session identifier
        """
        if not content.strip():
            return

        # Create searchable text representation
        # We augment it with role for context
        searchable_text = f"{role.upper()}: {content}"
        
        # Embed
        params = {"task_type": "RETRIEVAL_DOCUMENT"}
        # _embed_texts expects list
        vector = self._embed_texts([searchable_text], task_type="RETRIEVAL_DOCUMENT")
        
        # Add to FAISS
        self.index.add(vector)
        
        # Store metadata
        meta = {
            "role": role,
            "content": content, # Store raw content for retrieval
            "session_id": session_id,
            "timestamp": None # Could add timestamp
        }
        self.metadata.append(meta)
        
        # Auto-save after every add (for data safety, though adds latency)
        # Maybe better to save periodically? For now, instantaneous.
        self.save_memory()
        
    def save_memory(self):
        """Save the current index to disk."""
        try:
            self.save_index(self.index_dir)
        except Exception as e:
            print(f"Failed to save episodic memory: {e}")

    def recall(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant past interactions.
        Wrapper around search().
        """
        if self.index.ntotal == 0:
            return []
            
        return self.search(query, top_k=top_k)
