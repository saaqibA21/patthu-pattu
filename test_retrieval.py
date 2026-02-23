"""
Quick test of the RETRIEVAL part only (no API needed).
Shows which pages the model finds for each question.
"""
from pathu_pattu_model import PathuPattuRAG

rag = PathuPattuRAG("knowledge_base_ocr.json")
rag.load()

TESTS = [
    "What is Pathu Pattu?",
    "Thirumurugaatruppadai Nakkeerar",
    "shortest book Mullaipattu",
    "Karikal Chola Porunar",
    "Kurinji flowers mountain",
    "Puhar Kaveripoompattinam city",
    "U.V. Swaminatha Iyer palm leaf",
]

with open("retrieval_test.txt", "w", encoding="utf-8") as f:
    for q in TESTS:
        results = rag.search(q, top_k=3)
        f.write(f"\nQ: {q}\n")
        for chunk, score in results:
            f.write(f"  Page {chunk['page']} (score:{score:.4f}): {chunk['content'][:200]}\n")
        f.write("-"*60 + "\n")

print("Retrieval results -> retrieval_test.txt")
