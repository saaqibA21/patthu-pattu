"""
Cleans the existing OCR JSON files by removing excessive newlines.
Run this once to fix already-extracted data.
"""

import json
import re
import os

def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse 3+ consecutive newlines -> 2 (paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

files_to_clean = ["ocr_test_10pages.json", "knowledge_base_ocr.json"]

for fname in files_to_clean:
    if not os.path.exists(fname):
        print(f"⏭️  Skipping {fname} (not found)")
        continue
    
    print(f"🧹 Cleaning {fname}...")
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle different structures
    pages = data.get("pages", data.get("chunks", []))
    
    fixed = 0
    for page in pages:
        key = "content" if "content" in page else "text"
        if key in page:
            original = page[key]
            cleaned = clean_text(original)
            if cleaned != original:
                page[key] = cleaned
                fixed += 1
    
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Fixed {fixed} pages in {fname}")

print("\n✅ All done! JSON files are now clean.")
