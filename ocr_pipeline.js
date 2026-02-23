/**
 * PATHU PATTU - HIGH PRECISION OCR ENGINE
 * 
 * DESCRIPTION:
 * This script handles scanned PDF pages by converting them to high-resolution
 * images and applying Tesseract OCR with Tamil language support (tam).
 * 
 * NOTE: For 821 pages, we process in BATCHES to avoid memory crashes.
 */

const fs = require('fs');
const path = require('path');
const Tesseract = require('tesseract.js');

const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";
const OUTPUT_FILE = path.join(__dirname, 'knowledge_base_ocr.json');

async function runOCR(startPage, endPage) {
    console.log(`🚀 Starting OCR processing for pages ${startPage} to ${endPage}...`);

    try {
        // Step 1: Convert PDF pages to Images
        // Using dynamic import for ESM modules
        const pdfImg = await import('pdf-img-convert');

        // We use a high scale (2.0) for better OCR accuracy
        console.log("📸 Converting PDF pages to high-res images...");
        const pdfImages = await pdfImg.convert(PDF_PATH, {
            page_numbers: Array.from({ length: endPage - startPage + 1 }, (_, i) => i + startPage),
            base64: false,
            scale: 2.0
        });

        const results = [];

        // Step 2: Initialize Tesseract with Tamil (tam) + English (eng) support
        console.log("🧠 Initializing OCR Engine (Tamil + English)...");
        const worker = await Tesseract.createWorker('tam+eng');

        for (let i = 0; i < pdfImages.length; i++) {
            const pageNum = startPage + i;
            console.log(`📝 Processing Page ${pageNum}/${endPage}...`);

            // Perform OCR
            const { data: { text } } = await worker.recognize(pdfImages[i]);

            results.push({
                page: pageNum,
                content: text.trim()
            });

            // Intermediate save to prevent data loss
            saveProgress(results);
        }

        await worker.terminate();
        console.log("✅ Batch Processing Complete!");

    } catch (error) {
        console.error("❌ OCR Error:", error.message);
    }
}

function saveProgress(data) {
    let existingData = [];
    if (fs.existsSync(OUTPUT_FILE)) {
        try {
            existingData = JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8'));
        } catch (e) {
            existingData = [];
        }
    }

    // Merge new pages, avoiding duplicates
    const merged = [...existingData];
    data.forEach(newPage => {
        const index = merged.findIndex(p => p.page === newPage.page);
        if (index === -1) merged.push(newPage);
        else merged[index] = newPage;
    });

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(merged, null, 2));
}

// TEST RUN: Process page 1 to verify quality
if (require.main === module) {
    console.log("⚠️ Starting TEST RUN on Page 1...");
    runOCR(1, 1).then(() => {
        console.log("🏁 Test complete. Check 'knowledge_base_ocr.json' for results.");
    });
}

module.exports = { runOCR };
