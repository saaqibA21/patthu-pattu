/**
 * PATHU PATTU - ADVANCED AI TRAINING (LARGE PDF SUPPORT)
 * 
 * DESCRIPTION:
 * Uses the Gemini File API to upload the massive 90MB PDF
 * and then performs deep learning on the entire 821-page content.
 */

const fs = require('fs');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";

async function runAdvancedTraining() {
    try {
        console.log("📂 Step 1: Uploading large PDF to Gemini File API (90MB)...");

        const fileStats = fs.statSync(PDF_PATH);
        const fileData = fs.readFileSync(PDF_PATH);

        // 1. Initiate Resumable Upload
        console.log("📡 Initiating resumable upload session...");
        const uploadResponse = await fetch(`https://generativelanguage.googleapis.com/upload/v1beta/files?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'X-Goog-Upload-Protocol': 'resumable',
                'X-Goog-Upload-Command': 'start',
                'X-Goog-Upload-Header-Content-Length': fileStats.size,
                'X-Goog-Upload-Header-Content-Type': 'application/pdf',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file: {
                    display_name: "Pathu Pattu Full Text",
                    mime_type: "application/pdf"
                }
            })
        });

        if (!uploadResponse.ok) {
            const errorText = await uploadResponse.text();
            throw new Error(`Upload initiation failed: ${uploadResponse.status} ${errorText}`);
        }

        const uploadUrl = uploadResponse.headers.get('x-goog-upload-url');
        if (!uploadUrl) throw new Error("Could not get upload URL from Gemini API.");

        // 2. Upload the actual bytes
        console.log("⏳ Uploading bytes... This may take a moment for 90MB.");
        const finalUploadResponse = await fetch(uploadUrl, {
            method: 'POST',
            headers: {
                'Content-Length': fileStats.size,
                'X-Goog-Upload-Offset': 0,
                'X-Goog-Upload-Command': 'upload, finalize'
            },
            body: fileData
        });

        const finalResult = await finalUploadResponse.json();
        const fileUri = finalResult.file.uri;
        console.log(`✅ PDF Uploaded successfully! URI: ${fileUri}`);

        // 3. Process with Gemini 1.5 Flash
        console.log("🧠 Step 2: AI is now reading and analyzing all 821 pages...");

        const genResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [
                    {
                        parts: [
                            {
                                text: "You are the ultimate authority on Pathu Pattu (Sangam Literature). I have provided the full 821-page text. Please perform the following: 1. Extract the core essence and key verses of each of the 10 books. 2. Provide detailed historical context for each book. 3. Format this as a definitive knowledge base in Markdown. Provide everything in both Tamil and English."
                            },
                            {
                                file_data: {
                                    mime_type: "application/pdf",
                                    file_uri: fileUri
                                }
                            }
                        ]
                    }
                ]
            })
        });

        const genResult = await genResponse.json();

        if (genResult.candidates) {
            const output = genResult.candidates[0].content.parts[0].text;
            fs.writeFileSync('AI_MASTER_KNOWLEDGE.md', output);
            console.log("🏆 MISSION COMPLETE: The AI has mastered the PDF! Knowledge saved to AI_MASTER_KNOWLEDGE.md");
        } else {
            console.error("❌ AI Analysis failed:", JSON.stringify(genResult, null, 2));
        }

    } catch (error) {
        console.error("❌ Error during Advanced Training:", error.message);
    }
}

if (require.main === module) {
    runAdvancedTraining();
}
