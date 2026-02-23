/**
 * PATHU PATTU - KNOWLEDGE INGESTION PIPELINE
 * 
 * This script is responsible for:
 * 1. Extracting text from the 821-page PDF.
 * 2. Segmenting the text into logical chapters/verses.
 * 3. Saving the structured data into 'knowledge_base.json'.
 * 
 * REQUIRES: npm install pdf-parse
 */

const fs = require('fs');
const path = require('path');

// We use pdf-parse to extract text from the large PDF
// Since this is a large file, we handle it with care
async function ingestPDF(filePath) {
    try {
        const pdf = require('pdf-parse');

        console.log(`📂 Opening PDF: ${filePath}`);
        const dataBuffer = fs.readFileSync(filePath);

        console.log("⏳ Processing 821 pages... This may take a minute.");
        const data = await pdf(dataBuffer);

        console.log(`✅ Extraction Complete! Total Pages: ${data.numpages}`);

        // Structure the data for our 'Brain'
        const knowledgeData = {
            metadata: {
                source: "பத்துப்பாட்டு.pdf",
                pageCount: data.numpages,
                timestamp: new Date().toISOString()
            },
            fullText: data.text,
            // We will chunk this further in the future for the LLM
            chunks: segmentText(data.text)
        };

        const outputPath = path.join(__dirname, 'knowledge_base.json');
        fs.writeFileSync(outputPath, JSON.stringify(knowledgeData, null, 2));

        console.log(`🚀 Knowledge base saved to: ${outputPath}`);
        return knowledgeData;
    } catch (error) {
        if (error.code === 'MODULE_NOT_FOUND') {
            console.error("❌ Error: 'pdf-parse' not found.");
            console.log("👉 Please run: npm install pdf-parse");
        } else {
            console.error("❌ Error during ingestion:", error.message);
        }
    }
}

/**
 * Basic segmentation logic
 * Splits the 821 pages into manageable knowledge "atoms"
 */
function segmentText(text) {
    // Simple split by double newlines for now
    // In a real LLM setup, we'd use a more advanced chunking strategy
    return text.split('\n\n')
        .filter(chunk => chunk.trim().length > 50)
        .map((content, index) => ({
            id: `chunk_${index}`,
            content: content.trim()
        }));
}

// Target path provided by USER
const PDF_PATH = "C:\\Users\\SAAQIB\\OneDrive\\Desktop\\பத்துப்பாட்டு.pdf";

// Run the ingestion
if (require.main === module) {
    ingestPDF(PDF_PATH);
}

module.exports = { ingestPDF };
