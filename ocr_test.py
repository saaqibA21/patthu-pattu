"""
OCR Test - First 10 pages only
Quick test to verify Tamil OCR is working correctly.
"""

from pdf2image import convert_from_path
import pytesseract
import json
import os

PDF = r"C:\Users\SAAQIB\OneDrive\Desktop\பத்துப்பாட்டு.pdf"
OUTPUT = "ocr_test_10pages.json"
POPPLER_PATH = r"C:\Users\SAAQIB\AppData\Local\Temp\poppler\poppler-24.08.0\Library\bin"

print("=" * 50)
print("  OCR TEST - PAGES 1-10")
print("=" * 50)
print(f"\n📂 PDF: {os.path.basename(PDF)}")
print("📸 Converting pages 1-10 to images (DPI=150 for speed)...")

try:
    images = convert_from_path(
        PDF,
        dpi=150,
        first_page=1,
        last_page=10,
        fmt="jpeg",
        thread_count=4,
        poppler_path=POPPLER_PATH
    )
    print(f"✅ Got {len(images)} images. Starting OCR...\n")

    results = []
    total_chars = 0

    for i, img in enumerate(images):
        page_num = i + 1
        print(f"  🔍 Page {page_num}/10...", end="", flush=True)
        
        text = pytesseract.image_to_string(
            img, 
            lang="tam+eng",
            config="--oem 1 --psm 6"
        )
        text = text.strip()
        chars = len(text)
        total_chars += chars
        
        print(f" {chars} chars extracted")
        print(f"     Preview: {text[:100].replace(chr(10), ' ')}..." if text else "     (no text)")
        
        results.append({"page": page_num, "content": text, "chars": chars})

    # Save results
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"pages": results, "total_chars": total_chars}, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"✅ DONE! Total chars from 10 pages: {total_chars}")
    print(f"💾 Saved to: {OUTPUT}")
    
    if total_chars > 500:
        print("🎉 Tamil OCR is WORKING! Full 821-page processing is feasible.")
    else:
        print("⚠️  Very little text. May need higher DPI or different OCR settings.")

except Exception as e:
    print(f"\n❌ Error: {e}")
