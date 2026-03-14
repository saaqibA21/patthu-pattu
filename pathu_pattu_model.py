"""
PATHU PATTU RAG MODEL (Standalone)
====================================
Retrieval-Augmented Generation model that:
1. Loads your OCR-extracted knowledge base
2. Finds the most relevant pages for any question (semantic search)
3. Sends those pages as context to Gemini for a precise answer

This is STANDALONE — not connected to the website yet.
Test it here, then we'll plug it into the website later.
"""

import json
import re
import os
import math
from collections import defaultdict

class PathuPattuRAG:
    """
    RAG Model for Pathu Pattu Sangam Literature.
    Uses TF-IDF style retrieval + Gemini for generation.
    """
    
    def __init__(self, kb_path="knowledge_base_ocr.json"):
        self.chunks = []
        self.index = {}       # word -> [(chunk_id, freq), ...]
        self.idf = {}         # word -> inverse document freq
        self.loaded = False
        self.kb_path = kb_path
        
    def load(self):
        """Load and index the knowledge base."""
        if not os.path.exists(self.kb_path):
            print(f"❌ Knowledge base not found: {self.kb_path}")
            return False
        
        print(f"📚 Loading knowledge base: {self.kb_path}")
        with open(self.kb_path, encoding="utf-8") as f:
            data = json.load(f)
        
        pages = data.get("pages", [])
        print(f"  Found {len(pages)} pages total")
        
        # Only keep pages with meaningful content
        self.chunks = [
            {"id": f"page_{p['page']}", "page": p["page"], "content": p["content"]}
            for p in pages
            if p.get("char_count", 0) > 80
        ]
        print(f"  Indexing {len(self.chunks)} meaningful pages...")
        
        self._build_index()
        self.loaded = True
        print(f"  ✅ Index built with {len(self.index)} unique terms")
        return True
    
    def _tokenize(self, text):
        """Tokenize text into words (handles Tamil + English)."""
        # Split on whitespace and punctuation, keep Tamil Unicode chars
        words = re.findall(r'[\u0B80-\u0BFF]+|[a-zA-Z]+', text.lower())
        # Filter very short tokens
        return [w for w in words if len(w) > 1]
    
    def _build_index(self):
        """Build TF-IDF inverted index."""
        N = len(self.chunks)
        doc_freq = defaultdict(int)   # how many docs contain each word
        tf_map = {}                   # chunk_id -> {word: tf}
        
        for chunk in self.chunks:
            words = self._tokenize(chunk["content"])
            if not words:
                continue
            
            freq = defaultdict(int)
            for w in words:
                freq[w] += 1
            
            # TF = frequency / total words in doc
            tf_map[chunk["id"]] = {w: c / len(words) for w, c in freq.items()}
            
            for w in freq:
                doc_freq[w] += 1
        
        # IDF = log(N / df)
        self.idf = {w: math.log(N / df) for w, df in doc_freq.items() if df > 0}
        
        # Build inverted index: word -> [(chunk_id, tf-idf score), ...]
        self.index = defaultdict(list)
        for chunk in self.chunks:
            cid = chunk["id"]
            if cid not in tf_map:
                continue
            for word, tf in tf_map[cid].items():
                score = tf * self.idf.get(word, 0)
                if score > 0:
                    self.index[word].append((cid, score))
    
    def search(self, query, top_k=5):
        """
        Find the most relevant chunks for a query.
        Returns list of (chunk, score) tuples.
        """
        query_words = self._tokenize(query)
        
        # Accumulate scores
        scores = defaultdict(float)
        for word in query_words:
            if word in self.index:
                for chunk_id, score in self.index[word]:
                    scores[chunk_id] += score
        
        if not scores:
            return []
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Fetch top chunks
        chunk_map = {c["id"]: c for c in self.chunks}
        results = []
        for chunk_id, score in ranked[:top_k]:
            if chunk_id in chunk_map:
                results.append((chunk_map[chunk_id], score))
        
        return results
    
    def build_context(self, results, max_chars=6000):
        """Build context string from search results for the LLM."""
        context_parts = []
        total = 0
        
        for chunk, score in results:
            text = chunk["content"].strip()
            if not text:
                continue
            
            part = f"[பக்கம் {chunk['page']}]\n{text}"
            if total + len(part) > max_chars:
                # Truncate last chunk to fit
                remaining = max_chars - total
                if remaining > 100:
                    part = part[:remaining] + "..."
                    context_parts.append(part)
                break
            
            context_parts.append(part)
            total += len(part)
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_stats(self):
        """Return model statistics."""
        return {
            "total_chunks": len(self.chunks),
            "index_terms": len(self.index),
            "avg_chars": sum(len(c["content"]) for c in self.chunks) // max(len(self.chunks), 1)
        }


# ---- Gemini Query Function ----

import urllib.request
import json as _json

def ask_gemini(question, context, api_key, language="en"):
    """Send question + context to Gemini and return the answer."""
    
    lang_hint = "in Tamil (தமிழில்)" if language == "ta" else "in English"
    
    prompt = f"""You are Pattu LLM, an expert AI on Pathu Pattu (பத்துப்பாட்டு), the ten classical Sangam Tamil literary works. 
You were created by Mohammed Saaqib and his team.
Please answer clearly and professionally, breaking down ancient Tamil concepts with simplified meanings for better understanding.
If the text doesn't contain enough information, say so briefly and use your general knowledge to help.
Provide the answer {lang_hint}.

=== EXTRACTED BOOK TEXT (OCR) ===
{context}
=== END OF TEXT ===

User Question: {question}

Answer:"""

    payload = _json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }).encode("utf-8")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    req = urllib.request.Request(
        url, 
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = _json.loads(resp.read().decode("utf-8"))
    
    if result.get("candidates"):
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    error = result.get("error", {})
    return f"[API Error: {error.get('message', 'Unknown error')}]"


# ---- Main Model Entry Point ----

class PathuPattuModel:
    """
    The complete standalone model.
    Call model.answer(question) to get a response.
    """
    
    def __init__(self, api_key, kb_path="knowledge_base_ocr.json"):
        self.api_key = api_key
        self.rag = PathuPattuRAG(kb_path)
        self.ready = False
    
    def load(self):
        self.ready = self.rag.load()
        return self.ready
    
    def answer(self, question, language="en", top_k=5, verbose=False):
        """
        Answer a question using the OCR knowledge base.
        
        Args:
            question: The question to answer
            language: 'en' or 'ta'
            top_k: Number of relevant pages to retrieve
            verbose: If True, print retrieved pages too
        """
        if not self.ready:
            return "❌ Model not loaded. Call model.load() first."
        
        # Step 1: Retrieve relevant pages
        results = self.rag.search(question, top_k=top_k)
        
        if verbose:
            print(f"\n📄 Retrieved {len(results)} relevant pages:")
            for chunk, score in results:
                print(f"  Page {chunk['page']} (score: {score:.4f}) — {chunk['content'][:60]}...")
        
        if not results:
            return self._fallback(question, language)
        
        # Step 2: Build context
        context = self.rag.build_context(results)
        
        # Step 3: Ask Gemini
        try:
            return ask_gemini(question, context, self.api_key, language)
        except Exception as e:
            return f"[Error calling Gemini: {e}]"
    
    def _fallback(self, question, language):
        """Answer without context (general Sangam knowledge)."""
        try:
            prompt = f"You are Pattu LLM, an expert AI created by Mohammed Saaqib and his team. Answer questions about Pathu Pattu Sangam literature briefly with simplified meanings {'in Tamil' if language == 'ta' else 'in English'}: {question}"
            payload = _json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 512}
            }).encode("utf-8")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = _json.loads(resp.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"[Fallback error: {e}]"
    
    def stats(self):
        s = self.rag.get_stats()
        print(f"\n📊 Model Statistics:")
        print(f"  Pages indexed: {s['total_chunks']}")
        print(f"  Unique terms: {s['index_terms']:,}")
        print(f"  Avg chars/page: {s['avg_chars']:,}")
