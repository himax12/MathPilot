"""
FAISS Embedder for JEE Math Knowledge Base (Modern Version)

Uses:
- google-genai SDK (new) with text-embedding-004 model
- FAISS for vector similarity search

Usage:
    # Build index
    python -m backend.kb_builder.embedder build --kb-dir backend/knowledge/base/patterns
    
    # Search (in code)
    embedder = KBEmbedder()
    embedder.load_index("backend/knowledge/index")
    results = embedder.search("integrate sin^2(x) from 0 to pi", top_k=5)
"""

import json
import re
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any

import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("FAISS not available. Run: uv add faiss-cpu")

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("google-genai not available. Run: uv add google-genai")


class KBEmbedder:
    """
    Embeds JEE Math KB documents using Gemini text-embedding-004 model.
    Uses FAISS for vector similarity search.
    
    Modern version using google.genai SDK (not deprecated google.generativeai)
    """
    
    EMBEDDING_MODEL = "text-embedding-004"  # Latest Gemini embedding model
    EMBEDDING_DIMENSION = 768  # Default for text-embedding-004
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize embedder with Gemini API.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        if not FAISS_AVAILABLE:
            raise ImportError("faiss-cpu required. Run: uv add faiss-cpu")
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai required. Run: uv add google-genai")
        
        # Get API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # Initialize client
        self.client = genai.Client(api_key=self.api_key)
        
        self.index: Optional[faiss.IndexFlatL2] = None
        self.metadata: List[Dict[str, Any]] = []
        self.dimension = self.EMBEDDING_DIMENSION
    
    def _embed_texts(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> np.ndarray:
        """
        Embed texts using Gemini text-embedding-004.
        
        Args:
            texts: List of texts to embed
            task_type: RETRIEVAL_DOCUMENT for docs, RETRIEVAL_QUERY for queries
            
        Returns:
            NumPy array of embeddings
        """
        embeddings = []
        
        # Process in batches of 100 (API limit)
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            result = self.client.models.embed_content(
                model=self.EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.dimension
                )
            )
            
            # Extract embeddings from response
            for emb in result.embeddings:
                embeddings.append(emb.values)
            
            if i + batch_size < len(texts):
                print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} docs...")
        
        return np.array(embeddings).astype('float32')
    
    def _extract_doc_text(self, filepath: Path) -> str:
        """
        Extract searchable text from a KB document.
        Combines title, metadata, and key content.
        """
        content = filepath.read_text(encoding='utf-8')
        
        # Extract YAML frontmatter
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                yaml_content = parts[1].strip()
                for line in yaml_content.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        frontmatter[key.strip()] = val.strip()
                content = parts[2]
        
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filepath.stem
        
        # Get chapter and topic
        chapter = frontmatter.get('chapter', '').replace('-', ' ')
        topic = frontmatter.get('topic', '').replace('-', ' ')
        frequency = frontmatter.get('jee_frequency', '0')
        
        # Create searchable text (limit to avoid token limits)
        clean_content = re.sub(r'<[^>]+>', '', content)  # Remove HTML
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()[:800]
        
        searchable = f"""
        {title}
        Chapter: {chapter}
        Topic: {topic}
        JEE Frequency: {frequency} years
        {clean_content}
        """
        
        return searchable.strip()
    
    def _parse_frontmatter(self, filepath: Path) -> Dict[str, Any]:
        """Parse YAML frontmatter from KB doc for metadata."""
        content = filepath.read_text(encoding='utf-8')
        
        metadata = {
            "doc_id": filepath.stem,
            "file_path": str(filepath),
            "chapter": "",
            "topic": "",
            "jee_frequency": 0,
            "difficulty": "medium",
            "question_count": 0,
        }
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                yaml_content = parts[1].strip()
                for line in yaml_content.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        key = key.strip()
                        val = val.strip()
                        
                        if key == 'chapter':
                            metadata['chapter'] = val
                        elif key == 'topic':
                            metadata['topic'] = val
                        elif key == 'jee_frequency':
                            try:
                                metadata['jee_frequency'] = int(val)
                            except:
                                pass
                        elif key == 'difficulty':
                            metadata['difficulty'] = val
                        elif key == 'question_count':
                            try:
                                metadata['question_count'] = int(val)
                            except:
                                pass
        
        return metadata
    
    def build_index(self, kb_dir: str) -> int:
        """
        Build FAISS index from all KB documents in directory.
        
        Args:
            kb_dir: Path to KB documents directory
            
        Returns:
            Number of documents indexed
        """
        kb_path = Path(kb_dir)
        if not kb_path.exists():
            raise FileNotFoundError(f"KB directory not found: {kb_dir}")
        
        # Find all markdown files (excluding index)
        doc_files = [f for f in kb_path.glob("*.md") if not f.name.startswith('_')]
        
        if not doc_files:
            raise ValueError(f"No documents found in {kb_dir}")
        
        print(f"Building index from {len(doc_files)} documents...")
        print(f"Using model: {self.EMBEDDING_MODEL}")
        
        # Extract text and metadata
        texts = []
        self.metadata = []
        
        for filepath in doc_files:
            try:
                text = self._extract_doc_text(filepath)
                meta = self._parse_frontmatter(filepath)
                
                texts.append(text)
                self.metadata.append(meta)
            except Exception as e:
                print(f"  Warning: Could not process {filepath.name}: {e}")
        
        # Create embeddings using Gemini
        print("Creating embeddings with Gemini text-embedding-004...")
        embeddings = self._embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")
        
        # Build FAISS index
        print("Building FAISS index...")
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
        return self.index.ntotal
    
    def save_index(self, output_dir: str) -> None:
        """
        Save FAISS index and metadata to disk.
        
        Args:
            output_dir: Directory to save index files
        """
        if self.index is None:
            raise ValueError("No index to save. Call build_index first.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_file = output_path / "jee_math.index"
        faiss.write_index(self.index, str(index_file))
        
        # Save metadata
        metadata_file = output_path / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                "model": self.EMBEDDING_MODEL,
                "dimension": self.dimension,
                "documents": self.metadata
            }, f, indent=2)
        
        print(f"✅ Index saved to {output_path}")
        print(f"   - {index_file.name}: {index_file.stat().st_size / 1024:.1f} KB")
        print(f"   - {metadata_file.name}: {metadata_file.stat().st_size / 1024:.1f} KB")
    
    def load_index(self, index_dir: str) -> None:
        """
        Load existing FAISS index and metadata from disk.
        
        Args:
            index_dir: Directory containing index files
        """
        index_path = Path(index_dir)
        
        index_file = index_path / "jee_math.index"
        metadata_file = index_path / "metadata.json"
        
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found: {index_file}")
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
        
        # Load FAISS index
        self.index = faiss.read_index(str(index_file))
        
        # Load metadata
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.metadata = data.get("documents", [])
            self.dimension = data.get("dimension", self.EMBEDDING_DIMENSION)
        
        print(f"✅ Loaded index with {self.index.ntotal} vectors")
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        chapter_filter: Optional[str] = None,
        min_frequency: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant KB documents given a query.
        
        Args:
            query: Search query (natural language or math problem)
            top_k: Number of results to return
            chapter_filter: Optional - only return docs from this chapter
            min_frequency: Optional - only return docs with >= this JEE frequency
            
        Returns:
            List of matching documents with scores and metadata
        """
        if self.index is None:
            raise ValueError("No index loaded. Call load_index or build_index first.")
        
        # Embed query using RETRIEVAL_QUERY task type
        query_vector = self._embed_texts([query], task_type="RETRIEVAL_QUERY")
        
        # Search (get more results if filtering)
        search_k = min(top_k * 3, self.index.ntotal) if (chapter_filter or min_frequency) else top_k
        distances, indices = self.index.search(query_vector, search_k)
        
        # Build results with metadata
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            
            meta = self.metadata[idx]
            
            # Apply filters
            if chapter_filter and meta.get('chapter') != chapter_filter:
                continue
            if min_frequency and meta.get('jee_frequency', 0) < min_frequency:
                continue
            
            results.append({
                "doc_id": meta.get("doc_id", ""),
                "chapter": meta.get("chapter", ""),
                "topic": meta.get("topic", ""),
                "jee_frequency": meta.get("jee_frequency", 0),
                "difficulty": meta.get("difficulty", "medium"),
                "file_path": meta.get("file_path", ""),
                "score": float(dist),  # Lower is better for L2
                "similarity": 1.0 / (1.0 + float(dist))  # Convert to similarity
            })
            
            if len(results) >= top_k:
                break
        
        return results
    
    def get_document_content(self, doc_id: str) -> Optional[str]:
        """
        Get full content of a KB document by its ID.
        
        Args:
            doc_id: Document identifier (filename without extension)
            
        Returns:
            Full document content or None if not found
        """
        for meta in self.metadata:
            if meta.get("doc_id") == doc_id:
                filepath = Path(meta.get("file_path", ""))
                if filepath.exists():
                    return filepath.read_text(encoding='utf-8')
        return None


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FAISS KB Embedder (Gemini text-embedding-004)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build FAISS index from KB docs")
    build_parser.add_argument("--kb-dir", default="backend/knowledge/base/patterns",
                              help="Directory containing KB documents")
    build_parser.add_argument("--output", "-o", default="backend/knowledge/index",
                              help="Output directory for index files")
    
    # Search command (for testing)
    search_parser = subparsers.add_parser("search", help="Search the KB index")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--index-dir", default="backend/knowledge/index",
                               help="Directory containing index files")
    search_parser.add_argument("--top-k", type=int, default=5,
                               help="Number of results to return")
    
    args = parser.parse_args()
    
    if args.command == "build":
        embedder = KBEmbedder()
        count = embedder.build_index(args.kb_dir)
        embedder.save_index(args.output)
        print(f"\n✅ Successfully indexed {count} documents using Gemini text-embedding-004")
        
    elif args.command == "search":
        embedder = KBEmbedder()
        embedder.load_index(args.index_dir)
        
        print(f"\nSearching for: '{args.query}'")
        print("-" * 50)
        
        results = embedder.search(args.query, top_k=args.top_k)
        
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['chapter']}/{r['topic']}")
            print(f"   JEE Frequency: {r['jee_frequency']} years | Similarity: {r['similarity']:.3f}")
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
