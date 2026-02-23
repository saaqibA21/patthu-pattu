"""
PATHU PATTU — CUSTOM LOCAL AI MODEL
=====================================
THIS IS OUR OWN MODEL. No Gemini. No external API. 100% offline.

How it works:
1. Takes all 814 OCR pages from your PDF
2. Creates semantic "embeddings" (numerical fingerprints) for each chunk
3. When you ask a question, it finds the most relevant chunks using vector math
4. Returns the exact text from the book that answers your question

Model used for embeddings:
  sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  - Supports Tamil, English, and 50+ other languages
  - 120MB, runs fully offline on CPU
  - Trained to understand meaning, not just keywords

This is called "Semantic Search + Extractive QA" — it finds the EXACT 
passage in YOUR book that answers any question.

Run once to build: python build_model.py
Test it:          python test_local_model.py
"""

import json
import os
import numpy as np
import pickle
import re
import time

KB_PATH = "knowledge_base_ocr.json"
MODEL_DIR = "pathu_pattu_model_data"
INDEX_PATH = os.path.join(MODEL_DIR, "faiss_index.bin")
CHUNKS_PATH = os.path.join(MODEL_DIR, "chunks.pkl")
META_PATH = os.path.join(MODEL_DIR, "meta.json")

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 400       # characters per chunk
CHUNK_OVERLAP = 80     # overlap to avoid cutting sentences

def load_knowledge_base():
    print(f"📚 Loading OCR knowledge base...")
    with open(KB_PATH, encoding="utf-8") as f:
        data = json.load(f)
    pages = [p for p in data["pages"] if p.get("char_count", 0) > 80]
    print(f"  ✅ {len(pages)} usable pages loaded ({sum(p['char_count'] for p in pages):,} total chars)")
    return pages

def make_chunks(pages):
    """Split pages into overlapping smaller chunks for better retrieval."""
    chunks = []
    for page in pages:
        text = page["content"].strip()
        if not text:
            continue
        
        # Split into paragraphs first
        paragraphs = re.split(r"\n\n+", text)
        
        for para in paragraphs:
            para = para.strip()
            if len(para) < 50:
                continue
            
            # If paragraph is small enough, use as-is
            if len(para) <= CHUNK_SIZE:
                chunks.append({
                    "page": page["page"],
                    "text": para,
                })
            else:
                # Slide a window over longer paragraphs
                for start in range(0, len(para), CHUNK_SIZE - CHUNK_OVERLAP):
                    chunk_text = para[start:start + CHUNK_SIZE]
                    if len(chunk_text) < 50:
                        break
                    chunks.append({
                        "page": page["page"],
                        "text": chunk_text,
                    })
    
    print(f"  📦 Created {len(chunks)} text chunks from {len(pages)} pages")
    return chunks

def build_and_save():
    """Build the vector index from the knowledge base."""
    print("\n" + "="*55)
    print("  BUILDING PATHU PATTU CUSTOM AI MODEL")
    print("="*55)
    
    # Create output dir
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # 1. Load data
    pages = load_knowledge_base()
    
    # 2. Chunk
    print("\n📄 Creating text chunks...")
    chunks = make_chunks(pages)
    
    # 3. Load embedding model
    print(f"\n🔽 Loading multilingual embedding model...")
    print(f"   Model: {EMBEDDING_MODEL}")
    print(f"   (Downloads ~120MB once, then runs offline forever)")
    
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    print(f"  ✅ Embedding model loaded!")
    
    # 4. Create embeddings
    texts = [c["text"] for c in chunks]
    print(f"\n🧮 Creating embeddings for {len(texts)} chunks...")
    print(f"   This may take 5-10 minutes on CPU...")
    
    BATCH = 64
    all_embeddings = []
    for i in range(0, len(texts), BATCH):
        batch = texts[i:i+BATCH]
        embs = embedder.encode(batch, show_progress_bar=False, normalize_embeddings=True)
        all_embeddings.append(embs)
        done = min(i+BATCH, len(texts))
        pct = int(done / len(texts) * 100)
        print(f"  [{pct}%] {done}/{len(texts)} chunks embedded", end="\r")
    
    print(f"\n  ✅ All embeddings created!")
    
    embeddings = np.vstack(all_embeddings).astype("float32")
    dim = embeddings.shape[1]
    print(f"  Embedding dimension: {dim}")
    
    # 5. Build FAISS index
    print(f"\n📐 Building FAISS vector index...")
    import faiss
    index = faiss.IndexFlatIP(dim)   # Inner product = cosine similarity (since normalized)
    index.add(embeddings)
    print(f"  ✅ Index built with {index.ntotal} vectors")
    
    # 6. Save everything
    print(f"\n💾 Saving model to {MODEL_DIR}/...")
    faiss.write_index(index, INDEX_PATH)
    
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "embedding_model": EMBEDDING_MODEL,
            "total_chunks": len(chunks),
            "dimension": dim,
            "total_pages": len(pages),
            "built_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*55}")
    print("🏆 MODEL BUILT SUCCESSFULLY!")
    print(f"   Chunks indexed: {len(chunks)}")
    print(f"   Vector dimensions: {dim}")
    print(f"   Saved to: {MODEL_DIR}/")
    print(f"\nNext step: python test_local_model.py")

if __name__ == "__main__":
    build_and_save()
