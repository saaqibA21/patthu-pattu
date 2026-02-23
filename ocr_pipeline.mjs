/**
 * PATHU PATTU - HIGH PRECISION OCR ENGINE (ESM)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Tesseract from 'tesseract.js';
import pdfImg from 'pdf-img-convert';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";
const OUTPUT_FILE = path.join(__dirname, 'knowledge_base_ocr.json');

async function runOCR(startPage, endPage) {
    console.log(`🚀 Starting OCR processing for pages ${startPage} to ${endPage}...`);

    try {
        console.log("📸 Converting PDF pages to high-res images...");
        const pdfImages = await pdfImg.convert(PDF_PATH, {
            page_numbers: Array.from({ length: endPage - startPage + 1 }, (_, i) => i + startPage),
            base64: false,
            scale: 2.0
        });

        const results = [];

        console.log("🧠 Initializing OCR Engine (Tamil + English)...");
        // For ESM, Tesseract constructor is slightly different in some versions
        const worker = await Tesseract.createWorker('tam+eng');

        for (let i = 0; i < pdfImages.length; i++) {
            const pageNum = startPage + i;
            console.log(`📝 Processing Page ${pageNum}/${endPage}...`);

            const { data: { text } } = await worker.recognize(pdfImages[i]);

            results.push({
                page: pageNum,
                content: text.trim()
            });

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

    const merged = [...existingData];
    data.forEach(newPage => {
        const index = merged.findIndex(p => p.page === newPage.page);
        if (index === -1) merged.push(newPage);
        else merged[index] = newPage;
    });

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(merged, null, 2));
}

// TEST RUN
console.log("⚠️ Starting TEST RUN on Page 1...");
runOCR(1, 1).then(() => {
    console.log("🏁 Test complete. Check 'knowledge_base_ocr.json' for results.");
});
