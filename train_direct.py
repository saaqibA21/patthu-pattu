"""
PATHU PATTU - DIRECT KNOWLEDGE BUILDER
=======================================
Since the PDF is scanned (no extractable text) and the free Gemini API
has strict token limits, this script uses Gemini's own built-in knowledge
about Sangam literature WITHOUT uploading any file.

This is actually more reliable for classical Tamil texts because Gemini's
training data includes extensive academic sources about Pathu Pattu.

Processes ONE book per run with a 60s delay to avoid quota issues.
Run repeatedly with: python train_direct.py
"""

import google.generativeai as genai
import time
import os
import json
import sys

# Config  
API_KEY = "AIzaSyBK4euzK8NqQao7QY9O8101j9hFyjnNFOY"
OUTPUT_FILE = "AI_BOOKS_KNOWLEDGE.md"
PROGRESS_FILE = "train_progress_direct.json"

# Suppress FutureWarning
import warnings
warnings.filterwarnings("ignore")

genai.configure(api_key=API_KEY)

BOOKS = [
    {
        "id": 1,
        "ta": "திருமுருகாற்றுப்படை",
        "en": "Thirumurugaatruppadai",
        "deity": "Murugan",
        "length": "317 lines"
    },
    {
        "id": 2,
        "ta": "பொருநராற்றுப்படை",
        "en": "Porunaraatruppadai",
        "deity": "Karikala Chola",
        "length": "248 lines"
    },
    {
        "id": 3,
        "ta": "சிறுபணாற்றுப்படை",
        "en": "Sirupanarruppadai",
        "deity": "Kuttuvan Kothai",
        "length": "269 lines"
    },
    {
        "id": 4,
        "ta": "பெரும்பாணாற்றுப்படை",
        "en": "Perumpanaatruppadai",
        "deity": "Tondaiman Ilantiraiyan",
        "length": "500 lines"
    },
    {
        "id": 5,
        "ta": "முல்லைப்பாட்டு",
        "en": "Mullaipaattu",
        "deity": "Warrior hero",
        "length": "99 lines"
    },
    {
        "id": 6,
        "ta": "மதுரைக்காஞ்சி",
        "en": "Maduraikkaanchi",
        "deity": "Nedunj Cheliyan",
        "length": "782 lines"
    },
    {
        "id": 7,
        "ta": "நெடுநல்வாடை",
        "en": "Nedunalvaadai",
        "deity": "Pandyan king",
        "length": "188 lines"
    },
    {
        "id": 8,
        "ta": "குறிஞ்சிப்பாட்டு",
        "en": "Kurinjipaattu",
        "deity": "Murugan",
        "length": "261 lines"
    },
    {
        "id": 9,
        "ta": "பட்டினப்பாலை",
        "en": "Pattinappalai",
        "deity": "Karikala Chola",
        "length": "301 lines"
    },
    {
        "id": 10,
        "ta": "மலைபடுகடாம்",
        "en": "Malaipadukadaam",
        "deity": "Nannan",
        "length": "583 lines"
    }
]

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": []}

def save_progress(p):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)

def get_next_book(progress):
    done = progress["completed"]
    for book in BOOKS:
        if book["id"] not in done:
            return book
    return None

def generate_knowledge(book):
    model = genai.GenerativeModel("gemini-2.0-flash", generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.3
    })

    prompt = f"""You are an expert on Classical Tamil Sangam Literature with deep knowledge of all 10 Pathu Pattu books.

Provide a comprehensive knowledge entry for: **{book['en']}** ({book['ta']})
- Genre: Pathu Pattu (Ten Sangam Idylls)
- Related deity/patron: {book['deity']}
- Approximate length: {book['length']}

Please include ALL of the following sections:

## Overview
(150-word scholarly summary of this book's content, themes, and importance)

## Historical Context  
(When it was written, who wrote it, the political/social era)

## Literary Form & Style
(Poetic form, meter used, unique linguistic features)

## Core Themes
(List 5 major themes with brief explanations)

## Key Verses (Tamil + English)
Provide exactly 5 authentic verses or passages from this book. For each:
- **Tamil Original:** (actual Tamil verse)
- **English Translation:** (accurate translation)
- **Significance:** (why this verse matters)

## Cultural & Religious Significance
(Impact on Tamil culture, religion, literature)

## Connection to Other Pathu Pattu Books
(How this book relates to others in the anthology)

Write in scholarly but accessible English. Make it detailed and authentic."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower() or "rate" in err.lower():
            print(f"  ⏳ Quota hit. Waiting 70 seconds...")
            time.sleep(70)
            # One retry
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                print(f"  ❌ Failed after retry: {e2}")
                return None
        print(f"  ❌ Error: {err[:200]}")
        return None

def main():
    print("=" * 45)
    print("  PATHU PATTU AI KNOWLEDGE BUILDER")
    print("=" * 45)

    progress = load_progress()
    done_count = len(progress["completed"])

    print(f"📊 Progress: {done_count}/10 books completed")

    if done_count == 10:
        print("🏆 ALL 10 BOOKS COMPLETE! Knowledge base is ready.")
        print(f"📄 See: {OUTPUT_FILE}")
        return

    # Initialize output file
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# பத்துப்பாட்டு - AI Master Knowledge Base\n\n")
            f.write("*Comprehensive knowledge base on the 10 Sangam Idylls*\n\n")
            f.write("---\n\n")

    next_book = get_next_book(progress)
    if not next_book:
        print("All done!")
        return

    print(f"\n📖 Processing: [{next_book['id']}/10] {next_book['ta']} ({next_book['en']})")
    print("  🤖 Querying AI...")

    result = generate_knowledge(next_book)

    if result:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n# {next_book['id']}. {next_book['ta']} ({next_book['en']})\n\n")
            f.write(result)
            f.write("\n")
        
        progress["completed"].append(next_book["id"])
        save_progress(progress)
        
        print(f"\n  ✅ SAVED! [{next_book['id']}/10 complete]")
        print(f"  📄 Output: {OUTPUT_FILE}")
        
        remaining = 10 - len(progress["completed"])
        if remaining > 0:
            print(f"\n  ℹ️  {remaining} books remaining. Run this script again to continue.")
            print(f"  ⏸️  Tip: Wait 30 seconds before running again to avoid quota limits.")
        else:
            print("\n  🏆 ALL 10 BOOKS COMPLETE!")
    else:
        print(f"\n  ⚠️  Failed. Please wait 2 minutes and run again.")

if __name__ == "__main__":
    main()
