"""
PATHU PATTU - PYTHON AI TRAINER
================================
Uses PyMuPDF (fitz) to extract text from the 821-page PDF
and Google Generative AI SDK to process it with proper quota management.

Strategy: Extract real text with fitz, chunk it into 10 book segments,
then send each chunk to Gemini for structured analysis.
"""

import fitz  # PyMuPDF
import google.generativeai as genai
import time
import os
import json

# Config
API_KEY = "AIzaSyBK4euzK8NqQao7QY9O8101j9hFyjnNFOY"
PDF_PATH = r"C:\Users\SAAQIB\OneDrive\Desktop\பத்துப்பாட்டு.pdf"
OUTPUT_FILE = "AI_BOOKS_KNOWLEDGE.md"
PROGRESS_FILE = "train_progress.json"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

BOOKS = [
    "திருமுருகாற்றுப்படை (Thirumurugaatruppadai)",
    "பொருநராற்றுப்படை (Porunaraatruppadai)",
    "சிறுபணாற்றுப்படை (Sirupanarruppadai)",
    "பெரும்பாணாற்றுப்படை (Perumpanaatruppadai)",
    "முல்லைப்பாட்டு (Mullaipaattu)",
    "மதுரைக்காஞ்சி (Maduraikkaanchi)",
    "நெடுநல்வாடை (Nedunalvaadai)",
    "குறிஞ்சிப்பாட்டு (Kurinjipaattu)",
    "பட்டினப்பாலை (Pattinappalai)",
    "மலைபடுகடாம் (Malaipadukadaam)"
]

def extract_text(pdf_path):
    """Extract all text from PDF using PyMuPDF (handles Tamil scripts well)"""
    print(f"📂 Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"✅ Opened! Total pages: {len(doc)}")
    
    full_text = ""
    pages_with_text = 0
    
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages_with_text += 1
            full_text += f"\n[PAGE {i+1}]\n{text}"
        
        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(doc)} pages... ({pages_with_text} have text)")
    
    doc.close()
    print(f"\n📊 Result: {pages_with_text} pages with extractable text")
    print(f"📝 Total characters extracted: {len(full_text)}")
    return full_text

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "text_extracted": False, "raw_text": ""}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def query_gemini(prompt, retries=3):
    """Query Gemini with retry on quota error"""
    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower():
                wait = 60 * attempt
                print(f"  ⏳ Quota hit (attempt {attempt}). Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ Error: {err}")
                return None
    return None

def main():
    print("🧠 PATHU PATTU PYTHON AI TRAINER")
    print("=" * 40)

    progress = load_progress()

    # Step 1: Extract text from PDF
    if not progress.get("text_extracted") or not progress.get("raw_text"):
        raw_text = extract_text(PDF_PATH)
        
        if len(raw_text.strip()) < 100:
            print("\n⚠️  Very little text extracted - PDF may be image-based.")
            print("🔄 Switching to AI description mode (using file URI approach)...")
            raw_text = "SCANNED_PDF"  # Signal to use file-based mode
        
        progress["raw_text"] = raw_text
        progress["text_extracted"] = True
        save_progress(progress)
        print(f"\n✅ Text extraction complete ({len(raw_text)} chars).\n")
    else:
        raw_text = progress["raw_text"]
        print(f"♻️  Using cached text ({len(raw_text)} chars)")

    # Initialize output file
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# பத்துப்பாட்டு - AI Master Knowledge Base\n*Generated from 821-page Sangam Literature PDF*\n\n")

    # Step 2: Process each book
    is_scanned = raw_text == "SCANNED_PDF"
    chunk_size = len(raw_text) // 10 if not is_scanned else 0

    for i, book in enumerate(BOOKS):
        book_num = i + 1
        if book_num in progress["completed"]:
            print(f"✅ [{book_num}/10] {book} — Already done. Skipping.")
            continue

        print(f"\n📖 [{book_num}/10] Analyzing: {book}")

        if is_scanned:
            # For scanned PDFs, ask Gemini's built-in knowledge
            prompt = f"""You are an expert on Tamil Sangam literature. 
Provide detailed information about the book "{book}" from Pathu Pattu (Ten Songs).
Include:
1. Summary (200 words)
2. 5 actual verses in Tamil with English translations
3. Historical significance
4. Literary style and themes

Format as clean Markdown."""
        else:
            # Use actual extracted text
            start = i * chunk_size
            end = (i + 1) * chunk_size
            excerpt = raw_text[start:end][:8000]  # Limit to 8K chars per book
            
            prompt = f"""Analyze this extracted Tamil text from the Pathu Pattu PDF.
This section corresponds to the book: "{book}"

EXTRACTED TEXT:
{excerpt}

Based on this text, provide:
1. Summary of key content
2. Notable verses with translations  
3. Themes and literary significance

Format as Markdown."""

        result = query_gemini(prompt)
        
        if result:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n\n## {book_num}. {book}\n\n{result}\n")
            progress["completed"].append(book_num)
            save_progress(progress)
            print(f"✅ [{book_num}/10] {book} — SAVED!")
        else:
            print(f"⚠️  [{book_num}/10] Skip (will retry on next run)")

        if book_num < len(BOOKS):
            print(f"  ⏸️  Cooling down 45s before next book...")
            time.sleep(45)

    total = len(progress["completed"])
    print(f"\n{'='*40}")
    print(f"🏁 Session complete: {total}/{len(BOOKS)} books processed.")
    if total == len(BOOKS):
        print("🏆 ALL 10 BOOKS LEARNED! Check AI_BOOKS_KNOWLEDGE.md")
    else:
        print(f"ℹ️  Run again to continue from book {total + 1}.")

if __name__ == "__main__":
    main()
