"""
Batch test — saves results to test_results.txt to avoid encoding issues.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pathu_pattu_model import PathuPattuModel

API_KEY = "AIzaSyBK4euzK8NqQao7QY9O8101j9hFyjnNFOY"

TESTS = [
    ("What is Pathu Pattu?", "en"),
    ("Who wrote Thirumurugaatruppadai?", "en"),
    ("Who is Nakkeerar?", "en"),
    ("What is the shortest book in Pathu Pattu?", "en"),
    ("What is the longest book in Pathu Pattu?", "en"),
    ("Tell me about Karikal Chola", "en"),
    ("What flowers are mentioned in Kurinjipattu?", "en"),
    ("Describe the city of Puhar/Kaveripoompattinam", "en"),
    ("Who compiled Pathu Pattu from palm leaves?", "en"),
    ("What is Mullaipattu about?", "en"),
]

print("Loading model...")
model = PathuPattuModel(API_KEY)
ok = model.load()
if not ok:
    print("Failed to load!")
    sys.exit(1)

model.stats()
print("Running tests... (results -> test_results.txt)")

with open("test_results.txt", "w", encoding="utf-8") as out:
    out.write("PATHU PATTU AI MODEL — TEST RESULTS\n")
    out.write("=" * 60 + "\n\n")
    
    for i, (q, lang) in enumerate(TESTS, 1):
        print(f"  [{i}/{len(TESTS)}] {q}")
        try:
            answer = model.answer(q, language=lang, top_k=5)
            out.write(f"Q{i}: {q}\n")
            out.write(f"A: {answer}\n")
            out.write("-" * 60 + "\n\n")
        except Exception as e:
            out.write(f"Q{i}: {q}\nERROR: {e}\n\n")

print("Done! Open test_results.txt to see answers.")
