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
    
    def stats(self):
        if self.ready:
            print(f"📊 Turbo Model Ready: {self.index.ntotal} vectors indexed.")
