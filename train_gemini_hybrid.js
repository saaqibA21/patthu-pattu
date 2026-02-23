/**
 * PATHU PATTU - HYBRID AI TRAINING (CURL SUPPORT + RESUME)
 * 
 * DESCRIPTION:
 * Uses specialized CURL commands to handle the 90MB PDF upload
 * and includes a resume feature to save time.
 */

const { execSync } = require('child_process');
const fs = require('fs');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";

async function runHybridTraining() {
    try {
        let fileUri = "";

        // Check if we already uploaded this session
        if (fs.existsSync('last_upload_uri.txt')) {
            fileUri = fs.readFileSync('last_upload_uri.txt', 'utf8').trim();
            console.log(`♻️  Reusing existing upload session: ${fileUri}`);
        } else {
            console.log("🏁 Step 1: Initiating Upload Session...");
            const fileStats = fs.statSync(PDF_PATH);

            const initResponse = await fetch(`https://generativelanguage.googleapis.com/upload/v1beta/files?key=${API_KEY}`, {
                method: 'POST',
                headers: {
                    'X-Goog-Upload-Protocol': 'resumable',
                    'X-Goog-Upload-Command': 'start',
                    'X-Goog-Upload-Header-Content-Length': fileStats.size,
                    'X-Goog-Upload-Header-Content-Type': 'application/pdf',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file: { display_name: "Pathu Pattu Full Text", mime_type: "application/pdf" }
                })
            });

            const uploadUrl = initResponse.headers.get('x-goog-upload-url');
            console.log("🌊 Step 2: Streaming 90MB via CURL (High Stability)...");

            const curlCmd = `curl -X POST "${uploadUrl}" -H "X-Goog-Upload-Command: upload, finalize" -H "X-Goog-Upload-Offset: 0" --data-binary "@${PDF_PATH}"`;
            const uploadResultRaw = execSync(curlCmd).toString();
            const uploadResult = JSON.parse(uploadResultRaw);

            fileUri = uploadResult.file.uri;
            fs.writeFileSync('last_upload_uri.txt', fileUri);
            console.log(`✅ Upload Complete! URI: ${fileUri}`);
        }

        console.log("🧠 Step 3: AI is performing Deep Analysis on 821 pages...");
        console.log("⏳ Note: Finalizing master knowledge base...");

        const genResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [
                    {
                        parts: [
                            { text: "Analyze the uploaded 821-page Pathu Pattu PDF. Extract a concise summary and 3 unique verses for each of the 10 books. Include their Tamil text and English translation. Output in one single Markdown file." },
                            { file_data: { mime_type: "application/pdf", file_uri: fileUri } }
                        ]
                    }
                ]
            })
        });

        const genResult = await genResponse.json();

        if (genResult.candidates && genResult.candidates[0] && genResult.candidates[0].content) {
            const output = genResult.candidates[0].content.parts[0].text;
            fs.writeFileSync('AI_MASTER_KNOWLEDGE.md', output);
            console.log("🏆 SUCCESS: The AI has absorbed the 821-page PDF! Knowledge saved to AI_MASTER_KNOWLEDGE.md");
        } else {
            console.error("❌ AI Analysis did not return candidates. Full response:");
            console.error(JSON.stringify(genResult, null, 2));
        }

    } catch (error) {
        console.error("❌ Hybrid Training Failed:", error.message);
    }
}

runHybridTraining();
