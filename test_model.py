"""
PATHU PATTU MODEL — INTERACTIVE TEST CLI
==========================================
Tests the model BEFORE connecting it to the website.
Run: python test_model.py
"""

import sys
import io
# Fix Windows encoding for Tamil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathu_pattu_model import PathuPattuModel
import sys

API_KEY = "AIzaSyBK4euzK8NqQao7QY9O8101j9hFyjnNFOY"
KB_PATH = "knowledge_base_ocr.json"

def run_tests():
    """Run a set of automatic test questions to benchmark the model."""
    test_questions = [
        ("What is Pathu Pattu?", "en"),
        ("Who wrote Thirumurugaatruppadai?", "en"),
        ("Who is Nakkeerar?", "en"),
        ("What is the shortest book in Pathu Pattu?", "en"),
        ("பத்துப்பாட்டு என்றால் என்ன?", "ta"),
        ("திருமுருகாற்றுப்படை யார் எழுதினார்?", "ta"),
        ("மதுரைக்காஞ்சியில் எத்தனை வரிகள் உள்ளன?", "ta"),
    ]
    
    print("\n🧪 Running Automatic Tests...")
    print("=" * 55)
    
    for i, (question, lang) in enumerate(test_questions, 1):
        print(f"\n[Test {i}] {question}")
        answer = model.answer(question, language=lang, top_k=5)
        print(f"Answer: {answer[:300]}...")
        print("-" * 40)

def interactive_mode():
    """Launch an interactive Q&A loop."""
    print("\n" + "=" * 55)
    print("  🤖 PATHU PATTU AI — INTERACTIVE TEST MODE")
    print("=" * 55)
    print("Type your question and press Enter.")
    print("Commands: 'quit' = exit | 'test' = run tests | 'stats' = model info")
    print("Language: prefix with [ta] for Tamil. Example: [ta] முல்லைப்பாட்டு என்ன?")
    print("=" * 55)
    
    while True:
        try:
            user_input = input("\n❓ You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == "test":
            run_tests()
            continue
        
        if user_input.lower() == "stats":
            model.stats()
            continue
        
        # Detect language prefix
        lang = "en"
        question = user_input
        if user_input.startswith("[ta]"):
            lang = "ta"
            question = user_input[4:].strip()
        elif user_input.startswith("[en]"):
            lang = "en"
            question = user_input[4:].strip()
        # Auto-detect Tamil script
        elif any('\u0B80' <= c <= '\u0BFF' for c in user_input):
            lang = "ta"
        
        print(f"\n🔍 Searching {785} pages of Sangam literature...")
        answer = model.answer(question, language=lang, top_k=5, verbose=True)
        print(f"\n🤖 Answer:\n{answer}")

# ==============================
# MAIN
# ==============================
print("=" * 55)
print("  PATHU PATTU AI MODEL — LOADING")
print("=" * 55)

model = PathuPattuModel(API_KEY, KB_PATH)
print("\n⚙️  Loading and indexing knowledge base...")
ok = model.load()

if not ok:
    print("❌ Could not load knowledge base. Make sure OCR is complete.")
    sys.exit(1)

model.stats()
print("\n✅ Model ready! Starting interactive mode...\n")

# Check command-line args
if len(sys.argv) > 1 and sys.argv[1] == "--test":
    run_tests()
else:
    interactive_mode()
