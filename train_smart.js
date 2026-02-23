/**
 * PATHU PATTU - SMART AI TRAINER (WITH AUTO RETRY)
 * Reuses the already-uploaded PDF URI to avoid re-uploading 90MB.
 * Processes one book at a time with smart retry on quota errors.
 */

const fs = require('fs');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const FILE_URI = fs.readFileSync('last_upload_uri.txt', 'utf8').trim();
const OUTPUT_FILE = 'AI_BOOKS_KNOWLEDGE.md';

// Books to process — we track progress so we can resume
const BOOKS = [
    { id: 1, name: "திருமுருகாற்றுப்படை (Thirumurugaatruppadai)", prompt: "Thirumurugaatruppadai" },
    { id: 2, name: "பொருநராற்றுப்படை (Porunaraatruppadai)", prompt: "Porunaraatruppadai" },
    { id: 3, name: "சிறுபணாற்றுப்படை (Sirupanarruppadai)", prompt: "Sirupanarruppadai" },
    { id: 4, name: "பெரும்பாணாற்றுப்படை (Perumpanaatruppadai)", prompt: "Perumpanaatruppadai" },
    { id: 5, name: "முல்லைப்பாட்டு (Mullaipaattu)", prompt: "Mullaipaattu" },
    { id: 6, name: "மதுரைக்காஞ்சி (Maduraikkaanchi)", prompt: "Maduraikkaanchi" },
    { id: 7, name: "நெடுநல்வாடை (Nedunalvaadai)", prompt: "Nedunalvaadai" },
    { id: 8, name: "குறிஞ்சிப்பாட்டு (Kurinjipaattu)", prompt: "Kurinjipaattu" },
    { id: 9, name: "பட்டினப்பாலை (Pattinappalai)", prompt: "Pattinappalai" },
    { id: 10, name: "மலைபடுகடாம் (Malaipadukadaam)", prompt: "Malaipadukadaam" }
];

const PROGRESS_FILE = 'train_progress.json';

function loadProgress() {
    if (fs.existsSync(PROGRESS_FILE)) {
        return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
    }
    return { completed: [] };
}

function saveProgress(progress) {
    fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function queryGemini(bookName, bookPrompt, attempt = 1) {
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{
                    parts: [
                        {
                            text: `From the uploaded Pathu Pattu PDF, extract specific information about the book called "${bookPrompt}". 
                            Provide: 1) A 150-word summary. 2) 3 actual verses in Tamil script with English translation. 3) Historical context (50 words). 
                            Format neatly in Markdown. Be concise.`
                        },
                        { file_data: { mime_type: "application/pdf", file_uri: FILE_URI } }
                    ]
                }],
                generationConfig: { maxOutputTokens: 1024 }
            })
        });

        const result = await response.json();

        // Handle quota errors
        if (result.error && result.error.code === 429) {
            const retryDelay = result.error.details?.find(d => d.retryDelay)?.retryDelay || '60s';
            const delaySeconds = parseInt(retryDelay) + 10;
            console.log(`⏳ Quota hit. Waiting ${delaySeconds}s before retry (attempt ${attempt}/5)...`);
            await sleep(delaySeconds * 1000);
            if (attempt < 5) return queryGemini(bookName, bookPrompt, attempt + 1);
            return null;
        }

        if (result.candidates?.[0]?.content?.parts?.[0]?.text) {
            return result.candidates[0].content.parts[0].text;
        }

        console.error(`❌ Unexpected response for ${bookName}:`, JSON.stringify(result).substring(0, 200));
        return null;

    } catch (error) {
        console.error(`❌ Network error for ${bookName}:`, error.message);
        if (attempt < 3) {
            await sleep(15000);
            return queryGemini(bookName, bookPrompt, attempt + 1);
        }
        return null;
    }
}

async function runSmartTraining() {
    console.log("🧠 PATHU PATTU SMART AI TRAINER");
    console.log("================================");
    console.log(`📄 Using PDF URI: ${FILE_URI}`);
    console.log(`📚 Processing ${BOOKS.length} books...\n`);

    const progress = loadProgress();

    // Initialize output file
    if (!fs.existsSync(OUTPUT_FILE)) {
        fs.writeFileSync(OUTPUT_FILE, `# பத்துப்பாட்டு - AI Master Knowledge Base\n*Generated from 821-page PDF*\n\n`);
    }

    for (const book of BOOKS) {
        if (progress.completed.includes(book.id)) {
            console.log(`✅ [${book.id}/10] ${book.name} - Already done. Skipping.`);
            continue;
        }

        console.log(`\n📖 [${book.id}/10] Processing: ${book.name}...`);

        const text = await queryGemini(book.name, book.prompt);

        if (text) {
            fs.appendFileSync(OUTPUT_FILE, `\n\n---\n\n## ${book.id}. ${book.name}\n\n${text}\n`);
            progress.completed.push(book.id);
            saveProgress(progress);
            console.log(`✅ [${book.id}/10] ${book.name} - DONE!`);
        } else {
            console.log(`⚠️  [${book.id}/10] ${book.name} - Skipped (will retry next run).`);
        }

        // Smart delay: wait 45 seconds between books to stay under quota
        if (book.id < BOOKS.length && !progress.completed.includes(book.id + 1)) {
            console.log(`⏸️  Waiting 45s before next book...`);
            await sleep(45000);
        }
    }

    const totalDone = progress.completed.length;
    console.log(`\n🏁 Training session complete: ${totalDone}/10 books processed.`);

    if (totalDone === BOOKS.length) {
        console.log("🏆 ALL 10 BOOKS LEARNED! Check AI_BOOKS_KNOWLEDGE.md");
    } else {
        console.log(`ℹ️  Run this script again to continue from book ${totalDone + 1}.`);
    }
}

runSmartTraining();
