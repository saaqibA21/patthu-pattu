/**
 * PATHU PATTU - AI KNOWLEDGE INGESTION (GEMINI VISION)
 * 
 * DESCRIPTION:
 * Instead of local OCR, we use Gemini 1.5 Flash's native PDF support
 * to read and summarize the 821-page Sangam literature book.
 */

const fs = require('fs');
require('dotenv').config();

const API_KEY = process.env.GEMINI_API_KEY;
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}`;

const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";

async function trainFromPDF() {
    console.log("📜 AI Brain: Preparing to read the 821-page PDF...");

    try {
        const fileData = fs.readFileSync(PDF_PATH);
        const base64Data = fileData.toString('base64');

        console.log("🚀 Sending PDF to Gemini for deep learning...");

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                contents: [
                    {
                        parts: [
                            {
                                text: "You are an expert in Sangam literature. Read this 821-page Pathu Pattu PDF. Extract the most important verses, their meanings, and historical context. Summarize the content of each of the 10 books in detail. Output this as a structured JSON object that I can use as a knowledge base. Please provide the output in both Tamil and English."
                            },
                            {
                                inline_data: {
                                    mime_type: "application/pdf",
                                    data: base64Data
                                }
                            }
                        ]
                    }
                ],
                generationConfig: {
                    temperature: 0.2,
                    topP: 0.95,
                    topK: 40,
                    maxOutputTokens: 8192,
                }
            })
        });

        const result = await response.json();

        if (result.candidates && result.candidates[0].content) {
            const aiKnowledge = result.candidates[0].content.parts[0].text;
            fs.writeFileSync('ai_learned_knowledge.md', aiKnowledge);
            console.log("✅ AI successfully learned from the PDF! Knowledge saved to 'ai_learned_knowledge.md'.");
        } else {
            console.error("❌ AI could not process the PDF:", JSON.stringify(result, null, 2));
        }

    } catch (error) {
        console.error("❌ Error during AI Ingestion:", error.message);
    }
}

if (require.main === module) {
    if (!API_KEY) {
        console.error("❌ GEMINI_API_KEY not found in .env");
    } else {
        trainFromPDF();
    }
}
