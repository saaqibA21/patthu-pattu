/**
 * PATHU PATTU - CUSTOM KNOWLEDGE ENGINE (V1.0)
 * 
 * DESCRIPTION:
 * This is a standalone module designed to serve as the foundation for 
 * a custom AI model. It allows for indexing, searching, and generating
 * answers directly from the provided Sangam literature data.
 * 
 * Future Plan: Replace the 'query' method with an API call to a 
 * custom-trained LLM (BERT/Llama/Local GPT).
 */

class PathuPattuBrain {
    constructor() {
        this.knowledgeBase = {}; // Will hold the structured data
        this.index = [];         // For fast searching
        this.isLoaded = false;
    }

    /**
     * Step 1: DATA INGESTION
     * Loads the raw data from our internal database
     */
    async feedData(database) {
        console.log("🧠 Brain: Ingesting Pathu Pattu texts...");
        this.knowledgeBase = database;

        // Build a searchable index for faster retrieval
        Object.keys(this.knowledgeBase).forEach(id => {
            const entry = this.knowledgeBase[id];
            this.index.push({
                id: id,
                textTa: entry.fullTextTa?.toLowerCase() || "",
                textEn: entry.fullTextEn?.toLowerCase() || "",
                subjects: entry.sampleVersesTa || []
            });
        });

        // Check if we have an external knowledge base (from PDF)
        await this.loadExternalKnowledge();

        this.isLoaded = true;
        console.log(`✅ Brain: Knowledge base built with ${this.index.length} primary nodes.`);
    }

    async loadExternalKnowledge() {
        try {
            const fs = require('fs');
            const path = require('path');
            const kbPath = path.join(__dirname, 'knowledge_base.json');

            if (fs.existsSync(kbPath)) {
                console.log("📖 Brain: Loading extended knowledge from PDF...");
                const extendedKB = JSON.parse(fs.readFileSync(kbPath, 'utf8'));

                extendedKB.chunks.forEach(chunk => {
                    this.index.push({
                        id: chunk.id,
                        textTa: chunk.content.toLowerCase(),
                        textEn: "", // External PDF is primarily Tamil
                        isExternal: true
                    });
                });
                console.log(`📚 Brain: Added ${extendedKB.chunks.length} additional data points.`);
            }
        } catch (e) {
            console.warn("⚠️ Brain: Could not load external knowledge base yet.");
        }
    }

    /**
     * Step 2: PREPROCESSING (Local "Tokenizer")
     * Cleans up the user's question for better matching
     */
    preprocess(query) {
        return query.toLowerCase()
            .replace(/[?.!,]/g, '')
            .trim();
    }

    /**
     * Step 3: KNOWLEDGE RETRIEVAL (RAG - Lite)
     * Finds the most relevant piece of data for a given question
     */
    retrieve(query, lang = 'ta') {
        const cleanQuery = this.preprocess(query);
        let bestMatch = null;
        let highestScore = 0;
        let bestId = null;
        let isExternalMatch = false;

        this.index.forEach(item => {
            const targetText = lang === 'ta' ? item.textTa : item.textEn;
            const keywords = cleanQuery.split(' ');
            let score = 0;

            keywords.forEach(word => {
                if (word.length > 2 && targetText.includes(word)) {
                    score++;
                }
            });

            if (score > highestScore) {
                highestScore = score;
                bestId = item.id;
                isExternalMatch = !!item.isExternal;

                // If external, 'data' is the chunk itself
                if (isExternalMatch) {
                    bestMatch = { content: item.textTa };
                } else {
                    bestMatch = this.knowledgeBase[item.id];
                }
            }
        });

        return { data: bestMatch, score: highestScore, id: bestId, isExternal: isExternalMatch };
    }

    /**
     * Step 4: RESPONSE GENERATION
     * The "AI" part - currently logic-based, soon to be LLM-based.
     */
    generateAnswer(query, lang = 'ta') {
        if (!this.isLoaded) return "Brain not initialized yet.";

        const { data, score, isExternal } = this.retrieve(query, lang);

        if (score === 0 || !data) {
            return lang === 'ta'
                ? "மன்னிக்கவும், எனது தரவுத்தளத்தில் இதற்கான விடை இல்லை. உங்கள் சொந்த மாடல் தயாரானதும் இதை நான் இன்னும் சிறப்பாகப் பதிலளிப்பேன்."
                : "I couldn't find a specific match in the current data. Once our custom LLM is ready, I will be able to synthesize an answer specialized for this query.";
        }

        // If it's external data (from PDF)
        if (isExternal) {
            return lang === 'ta'
                ? `[PDF ஆதாரத்திலிருந்து]:\n\n${data.content}`
                : `[From PDF source]:\n\n${data.content}`;
        }

        // Internal data (from database)
        const response = lang === 'ta'
            ? `[நூலகத் தரவு]:\n\n${data.fullTextTa.substring(0, 500)}...`
            : `[Library Data]:\n\n${data.fullTextEn.substring(0, 500)}...`;

        return response;
    }
}

// Export for future use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PathuPattuBrain;
} else {
    // For browser testing
    const customBrain = new PathuPattuBrain();
    console.log("🚀 Custom Knowledge Model initialized. Ready to be trained!");
}
