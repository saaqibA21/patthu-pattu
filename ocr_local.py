"""
PATHU PATTU - LOCAL OCR ENGINE (NO API QUOTAS)
================================================
Uses Tesseract 5.5 with Tamil language model (tam.traineddata)
+ pdf2image to convert PDF pages to images for OCR.

No internet required. No API quotas. 100% local processing.

Run: python ocr_local.py
Resume: It saves progress after every 10 pages - safe to Ctrl+C and continue.
"""

import pytesseract
from pdf2image import convert_from_path
import json
import os
import sys
import time
import re

def clean_text(text):
    """Clean OCR output: collapse excessive whitespace while keeping paragraph flow."""
    if not text:
        return ""
    # Replace \r\n and \r with \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse 3+ consecutive newlines into 2 (one paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Within a paragraph, join lines that don't end with punctuation
    # (avoids merging intentional verse line breaks)
    lines = text.split("\n")
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        clean_lines.append(stripped)
    # Rebuild — keep empty lines as paragraph separators
    text = "\n".join(clean_lines)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # Final strip
    return text.strip()

# Configuration
PDF_PATH = r"C:\Users\SAAQIB\OneDrive\Desktop\பத்துப்பாட்டு.pdf"
OUTPUT_JSON = "knowledge_base_ocr.json"
PROGRESS_FILE = "ocr_progress.json"
POPPLER_PATH = r"C:\Users\SAAQIB\AppData\Local\Temp\poppler\poppler-24.08.0\Library\bin"

# Tesseract OCR settings for Tamil
TESSERACT_CONFIG = r"--oem 1 --psm 6"  # LSTM engine, block text mode
LANG = "tam+eng"  # Tamil + English

# Process in batches of 10 pages
BATCH_SIZE = 10
# DPI: higher = better accuracy but slower (200 is good for Tamil)
DPI = 200

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_page": 0, "total_pages": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)

def load_results():
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metadata": {"source": "பத்துப்பாட்டு.pdf"}, "pages": []}

def save_results(results):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def count_pages():
    """Quick page count using fitz (no image conversion needed)"""
    try:
        import fitz
        doc = fitz.open(PDF_PATH)
        count = len(doc)
        doc.close()
        return count
    except:
        # Fallback: convert just 1 page to get started
        return 821  # Known page count

def ocr_page_batch(start_page, end_page):
    """Convert a batch of PDF pages to images and run OCR"""
    results = []
    
    try:
        print(f"  📸 Converting pages {start_page}-{end_page} to images (DPI={DPI})...")
        images = convert_from_path(
            PDF_PATH,
            dpi=DPI,
            first_page=start_page,
            last_page=end_page,
            fmt="jpeg",
            thread_count=2,
            poppler_path=POPPLER_PATH
        )
        
        for i, image in enumerate(images):
            page_num = start_page + i
            print(f"  🔍 OCR on page {page_num}...", end="", flush=True)
            
            start_time = time.time()
            text = pytesseract.image_to_string(image, lang=LANG, config=TESSERACT_CONFIG)
            elapsed = time.time() - start_time
            
            text = clean_text(text)  # Clean excessive newlines
            char_count = len(text)
            
            print(f" {char_count} chars [{elapsed:.1f}s]")
            
            results.append({
                "page": page_num,
                "content": text,
                "char_count": char_count
            })
        
        return results
        
    except Exception as e:
        print(f"\n  ❌ Error on pages {start_page}-{end_page}: {e}")
        return []

def get_summary_stats(results):
    pages_with_text = [p for p in results["pages"] if p["char_count"] > 50]
    total_chars = sum(p["char_count"] for p in results["pages"])
    return len(pages_with_text), total_chars

def main():
    print("=" * 55)
    print("  PATHU PATTU LOCAL OCR ENGINE")
    print("  Tesseract v5.5 + Tamil Language Model")
    print("=" * 55)
    
    # Check PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"\n❌ PDF not found: {PDF_PATH}")
        sys.exit(1)
    
    # Load progress
    progress = load_progress()
    results = load_results()
    
    # Get total pages
    if progress["total_pages"] == 0:
        print("\n📂 Scanning PDF...")
        total_pages = count_pages()
        progress["total_pages"] = total_pages
        save_progress(progress)
    else:
        total_pages = progress["total_pages"]
    
    start_from = progress["last_page"] + 1
    
    print(f"\n📄 PDF: {os.path.basename(PDF_PATH)}")
    print(f"📊 Total pages: {total_pages}")
    print(f"▶️  Starting from page: {start_from}")
    print(f"🌐 OCR Language: Tamil + English")
    
    if start_from > total_pages:
        print("\n✅ All pages already processed!")
        pages_with_text, total_chars = get_summary_stats(results)
        print(f"📈 Pages with text: {pages_with_text}/{total_pages}")
        print(f"📝 Total characters extracted: {total_chars:,}")
        return
    
    remaining = total_pages - start_from + 1
    estimated_min = (remaining * 8) // 60  # ~8 seconds per page at DPI=200
    print(f"⏱️  Estimated time: ~{estimated_min} minutes for {remaining} pages")
    print(f"\n💡 Tip: You can press Ctrl+C anytime. Progress is saved every {BATCH_SIZE} pages.\n")
    
    # Process in batches
    try:
        for batch_start in range(start_from, total_pages + 1, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE - 1, total_pages)
            pct = int((batch_start / total_pages) * 100)
            
            print(f"\n📖 Batch {batch_start}-{batch_end} of {total_pages} ({pct}% done)")
            
            batch_results = ocr_page_batch(batch_start, batch_end)
            
            if batch_results:
                results["pages"].extend(batch_results)
                progress["last_page"] = batch_end
                save_progress(progress)
                save_results(results)
                
                pages_done = batch_end - start_from + 1
                batch_chars = sum(r["char_count"] for r in batch_results)
                print(f"  ✅ Saved! Batch had {batch_chars:,} chars. Total pages: {batch_end}/{total_pages}")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  OCR paused. Run again to resume from where you left off.")
        return
    
    # Done!
    print("\n" + "=" * 55)
    print("🏆 OCR COMPLETE!")
    pages_with_text, total_chars = get_summary_stats(results)
    print(f"📈 Pages with text: {pages_with_text}/{total_pages}")
    print(f"📝 Total characters extracted: {total_chars:,}")
    print(f"💾 Saved to: {OUTPUT_JSON}")
    
    # Update the main knowledge_base.json
    kb = {
        "metadata": {
            "source": "பத்துப்பாட்டு.pdf (OCR processed)",
            "pageCount": total_pages,
            "pagesWithText": pages_with_text,
            "totalChars": total_chars
        },
        "fullText": "\n\n".join(
            f"[PAGE {p['page']}] {p['content']}" 
            for p in results["pages"] 
            if p["char_count"] > 50
        ),
        "chunks": [
            {"id": f"page_{p['page']}", "content": clean_text(p["content"])}
            for p in results["pages"]
            if p["char_count"] > 50
        ]
    }
    
    with open("knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    
    print("✅ knowledge_base.json updated — AI Brain can now use this data!")

if __name__ == "__main__":
    main()
