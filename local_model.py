"""
PATHU PATTU — LOCAL MODEL INFERENCE ENGINE
===========================================
Loads the custom-built vector model and answers questions.
100% offline. No API calls. Answers come from YOUR OCR data.
"""

import json
import os
import numpy as np
import pickle
import re

MODEL_DIR = "pathu_pattu_model_data"
INDEX_PATH = os.path.join(MODEL_DIR, "faiss_index.bin")
CHUNKS_PATH = os.path.join(MODEL_DIR, "chunks.pkl")
META_PATH = os.path.join(MODEL_DIR, "meta.json")

class LocalPathuPattuModel:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.ready = False
        self.model_name = "text-embedding-3-small"
    
    def load(self):
        turbo_index = "pathu_pattu_model_data/faiss_index_turbo.bin"
        if not os.path.exists(turbo_index): return False
        
        import faiss
        self.index = faiss.read_index(turbo_index)
        with open("pathu_pattu_model_data/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)
        
        self.ready = True
        print(f"🚀 TURBO ENGINE LOADED: {self.index.ntotal} vectors")
        return True
    
    def search(self, query, top_k=5):
        if not self.ready: return []
        
        # Use OpenAI to embed the query instead of local CPU
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        try:
            resp = client.embeddings.create(input=[query], model=self.model_name)
            q_emb = np.array([resp.data[0].embedding], dtype="float32")
            
            scores, indices = self.index.search(q_emb, top_k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx >= 0:
                    results.append({"text": self.chunks[idx]["text"], "page": self.chunks[idx]["page"], "score": float(score)})
            return results
        except Exception as e:
            print(f"Turbo Search Error: {e}")
            return []
    
    def search(self, query, top_k=8):
        """Find the most relevant chunks for a query."""
        # Embed the question
        q_embedding = self.embedder.encode([query], normalize_embeddings=True)
        q_embedding = np.array(q_embedding, dtype="float32")
        
        # Search in FAISS
        scores, indices = self.index.search(q_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and score > 0.1:   # Minimum similarity threshold
                chunk = self.chunks[idx]
                results.append({
                    "text": chunk["text"],
                    "page": chunk["page"],
                    "score": float(score)
                })
        
        return results
    
    def answer(self, question, top_k=8, verbose=False):
        """
        Answer a question purely from the book text.
        Returns (answer_text, pages_used, confidence)
        """
        if not self.ready:
            return "Model not loaded.", [], 0.0
        
        results = self.search(question, top_k=top_k)
        
        if not results:
            return "இந்தக் கேள்விக்கு பதில் புத்தகத்தில் கிடைக்கவில்லை. (No relevant content found in the book.)", [], 0.0
        
        if verbose:
            print(f"\n  Found {len(results)} relevant passages:")
            for r in results[:3]:
                print(f"  [Page {r['page']}, score={r['score']:.3f}] {r['text'][:80]}...")
        
        # Build a structured answer from the retrieved passages
        pages_used = sorted(set(r["page"] for r in results))
        top_score = results[0]["score"] if results else 0.0
        
        # Format answer: show the best matching passages
        answer_parts = []
        seen_text = set()
        
        for r in results[:5]:
            # Deduplicate similar content
            snippet = r["text"][:100]
            if snippet not in seen_text:
                seen_text.add(snippet)
                answer_parts.append(f"[பக்கம் {r['page']}] {r['text']}")
        
        formatted = "\n\n".join(answer_parts)
        return formatted, pages_used, top_score
    
    def stats(self):
        if self.ready:
            print(f"\n📊 Model Stats:")
            print(f"  Chunks: {self.meta['total_chunks']}")
            print(f"  Pages:  {self.meta['total_pages']}")
            print(f"  Dim:    {self.meta['dimension']}")
            print(f"  Built:  {self.meta.get('built_at', 'unknown')}")
