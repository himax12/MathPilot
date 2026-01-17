"""Quick test for FAISS search"""
from backend.kb_builder.embedder import KBEmbedder

e = KBEmbedder()
e.load_index('backend/knowledge/index')

results = e.search('integrate sin^2(x) from 0 to pi', top_k=5)


print("\nSearch Results written to test_results.txt")
with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write("Search Results:\n")
    f.write("-" * 60 + "\n")
    for i, r in enumerate(results, 1):
        f.write(f"{i}. {r['chapter']}/{r['topic']}\n")
        f.write(f"   Similarity: {r['similarity']:.3f} | JEE Freq: {r['jee_frequency']} yrs\n")

