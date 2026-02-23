/**
 * PATHU PATTU - SECTIONAL AI TRAINING
 * 
 * DESCRIPTION:
 * Processes the 821-page PDF book by book to avoid quota limits.
 */

const fs = require('fs');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const URI_FILE = 'last_upload_uri.txt';

async function runSectionalTraining() {
    try {
        if (!fs.existsSync(URI_FILE)) {
            console.error("❌ No upload URI found. Please run hybrid training first.");
            return;
        }
        const fileUri = fs.readFileSync(URI_FILE, 'utf8').trim();
        console.log(`♻️  Using existing PDF: ${fileUri}`);

        const books = [
            "Thirumurugaatruppadai", "Porunaraatruppadai", "Sirupanaatruppadai",
            "Perumpanaatruppadai", "Mullaipaattu", "Maduraikaanchi",
            "Nedunalvaadai", "Kurinchipaattu", "Pattinappaalai", "Malaipadukadaam"
        ];

        console.log("📚 Starting Sectional Deep Learning...");

        for (const book of books) {
            console.log(`📖 Learning about: ${book}...`);

            const genResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [
                        {
                            parts: [
                                { text: `Extract all key information for the book "${book}" from the uploaded 821-page PDF. Include its central theme, 3 main verses in Tamil/English, and historical significance. Format as Markdown.` },
                                { file_data: { mime_type: "application/pdf", file_uri: fileUri } }
                            ]
                        }
                    ]
                })
            });

            const genResult = await genResponse.json();

            if (genResult.candidates) {
                const output = genResult.candidates[0].content.parts[0].text;
                fs.appendFileSync('AI_BOOKS_KNOWLEDGE.md', `\n\n# ${book}\n${output}`);
                console.log(`✅ ${book} Learned!`);
            } else {
                console.error(`❌ Failed to learn ${book}:`, JSON.stringify(genResult, null, 2));
                break; // Stop to avoid hitting quota again
            }

            // Wait 10 seconds between books to stay safe
            console.log("🛑 Cooling down for 10s...");
            await new Promise(r => setTimeout(r, 10000));
        }

        console.log("🏆 Sectional Training Complete! Check AI_BOOKS_KNOWLEDGE.md");

    } catch (error) {
        console.error("❌ Sectional Training Failed:", error.message);
    }
}

runSectionalTraining();
