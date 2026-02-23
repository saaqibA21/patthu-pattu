// PATHU PATTU AI CHATBOT - ADVANCED SCHOLAR RAG (OPENAI POWERED)
// Intelligent retrieval-augmented generation backend

const CHAT_CONFIG = {
    // Connects to local server for dev, or the Render production backend
    serverUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:3000/api/chat'
        : 'https://patthu-pattu.onrender.com/api/chat'
};


// ==============================================
// PATHU PATTU KNOWLEDGE BASE
// ==============================================
const PATHU_PATTU_CONTEXT = `You are an expert AI assistant specializing in Pathu Pattu (பத்துப்பாட்டு), the ten classical Tamil literary works from the Sangam period.

KNOWLEDGE BASE:

1. திருமுருகாற்றுப்படை (Thirumurugaatruppadai)
   - Poet: நக்கீரர் (Nakkeerar)
   - Lines: 317
   - Theme: Devotion to Lord Murugan (Arupadai Veedu)
   - Abodes: Thirupparankundram, Thiruchendur, Palani, Swamimalai, Thiruthani, Pazhamudhirsolai.

2. பொருநராற்றுப்படை (Porunararruppadai)
   - Poet: முடத்தாமக்கன்னியார் (Mudathama Kanniyar)
   - Lines: 248
   - Theme: Praise of King Karikal Chola (Battle of Venni).

3. சிறுபாணாற்றுப்படை (Sirupanarruppadai)
   - Poet: நத்தத்தனார் (Nattattanar)
   - Lines: 269
   - Theme: Nalliyakodan's generosity; features bards with small lutes.

4. பெரும்பாணாற்றுப்படை (Perumpanarruppadai)
   - Poet: உருத்திரங்கண்ணனார் (Uruthirankannanar)
   - Lines: 500
   - Theme: Thondaiman Ilandhirayan of Kanchipuram; features bards with large lutes.

5. முல்லைப்பாட்டு (Mullaipattu)
   - Poet: நப்பூதனார் (Napputanar)
   - Lines: 103 (Shortest!)
   - Theme: Akam (Interior) - Patiently waiting for the hero's return from war.

6. நெடுநல்வாடை (Nedunalvadai)
   - Poet: நக்கீரர் (Nakkeerar)
   - Lines: 188
   - Theme: The cold north wind; separation of Queen from King Nedunchezhiyan.

7. மதுரைக்காஞ்சி (Maduraikanchi)
   - Poet: மாங்குடி மருதனார் (Mangudi Maruthanar)
   - Lines: 782 (Longest!)
   - Theme: Advice to King Nedunchezhiyan on the transience of life; glorious Madurai description.

8. குறிஞ்சிப்பாட்டு (Kurinjippattu)
   - Poet: கபிலர் (Kapilar)
   - Lines: 261
   - Theme: Secret love in the mountains; showcases many types of mountain flowers (99 flowers).

9. பட்டினப்பாலை (Pattinappalai)
   - Poet: உருத்திரங்கண்ணனார் (Uruthirankannanar)
   - Lines: 301
   - Theme: Description of Puhar (Kaveripoompattinam) and Chola king Karikal Peruvalathan.

10. மலைபடுகடாம் (Malaipadukadam)
    - Poet: இரணியமுட்டத்துப் பெருங்குன்றூர் பெருங்கௌசிகனார்
    - Lines: 583
    - Theme: Nannan's heroism; description of mountain acoustics (Mountain Echoes).

HISTORICAL SIGNIFICANCE:
- Sangam Era (300 BCE - 300 CE)
- Rediscovered by: U.V. Swaminatha Iyer (the Grandfather of Tamil) from palm leaf manuscripts.
- Total Lines: 3,237 lines of Agaval meter.
- Categorization: 10 medium-length poems of the Ettuthokai-Pathupattu collection.

ANSWER GUIDELINES:
- Respond in the user's language (Tamil or English).
- Be polite, historical, and detailed.
- If the API key is missing, inform the user subtly while providing a manual fallback answer.
`;

// ==============================================
// AI CHATBOT FUNCTIONS
// ==============================================

class PathuPattuAI {
    constructor() {
        this.conversationHistory = [];
        this.feedbackData = [];
    }

    async ask(userQuestion, language = 'ta') {
        try {
            // Call our local backend instead of Google directly
            const response = await fetch(CHAT_CONFIG.serverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userQuestion,
                    language: language
                })
            });

            if (response.status === 503) {
                const initData = await response.json().catch(() => ({}));
                return {
                    answer: `📚 **${language === 'ta' ? 'அறிஞராக மாறிக் கொண்டிருக்கிறேன்...' : 'I am currently studying the books...'}**\n\n${initData.message || ''}\n\n--- \n**${language === 'ta' ? 'இப்போதைக்கு எனக்குத் தெரிந்த தகவல்:' : 'In the meantime, here is what I know:'}**\n${this.getSmartFallback(userQuestion, language)}`,
                    engine: 'Studying...'
                };
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.warn('Backend server error:', errorData);
                return {
                    answer: this.getSmartFallback(userQuestion, language),
                    engine: 'Local Fallback'
                };
            }

            const data = await response.json();

            if (data.answer) {
                this.logInteraction(userQuestion, data.answer, language);
                return {
                    answer: data.answer,
                    pages: data.pages,
                    engine: data.engine
                };
            } else {
                return {
                    answer: this.getSmartFallback(userQuestion, language),
                    engine: 'Local Fallback'
                };
            }

        } catch (error) {
            console.warn('Could not connect to backend server:', error);
            const slowMessage = language === 'ta'
                ? "மன்னிக்கவும், எனது அறிவுத் தளம் தற்போது விழித்துக் கொள்கிறது (Render Free Tier). தயவுசெய்து 60 வினாடிகள் கழித்து மீண்டும் முயற்சிக்கவும்..."
                : "The AI Scholar is currently waking up from its library (Render Free Tier). Please wait about 60 seconds for the initial load and try again...";

            return {
                answer: slowMessage + "\n\n**இப்போதைக்கு எனக்கு தெரிந்தவை / For now, I know:**\n" + this.getSmartFallback(userQuestion, language),
                engine: 'Waking Up...'
            };
        }
    }

    getSmartFallback(question, language) {
        const q = question.toLowerCase();

        // 1. Basic Books Matching
        const bookMatches = {
            'திருமுருகாற்றுப்படை': { ta: 'திருமுருகாற்றுப்படை நக்கீரரால் இயற்றப்பட்டது. இது முருகனின் ஆறு படைவீடுகளைப் பற்றி விவரிக்கிறது.', en: 'Thirumurugaatruppadai was composed by Nakkeerar. It describes the six abodes of Lord Murugan.' },
            'பொருநராற்றுப்படை': { ta: 'பொருநராற்றுப்படை கரிகால் சோழனைப் புகழ்ந்து பாடப்பட்ட நூல்.', en: 'Porunararruppadai celebrates the glory of Chola king Karikal Cholan.' },
            'சிறுபாணாற்றுப்படை': { ta: 'சிறுபாணாற்றுப்படை நல்லியக்கோடனின் கொடைத்திறத்தைப் பற்றிப் பாடுகிறது.', en: 'Sirupanarruppadai speaks of King Nalliyakodan\'s generosity.' },
            'பெரும்பாணாற்றுப்படை': { ta: 'பெரும்பாணாற்றுப்படை தொண்டைமான் இளந்திரையனைப் பற்றிப் பாடுகிறது.', en: 'Perumpanarruppadai is about King Thondaiman Ilandhirayan.' },
            'முல்லைப்பாட்டு': { ta: 'முல்லைப்பாட்டு பத்துப்பாட்டில் மிகச் சிறிய நூல் (103 வரிகள்). கார் காலத்தில் தலைவி தலைவனுக்காகக் காத்திருப்பதை இது விவரிக்கிறது.', en: 'Mullaipattu is the shortest (103 lines), describing a wife waiting for her hero during the rainy season.' },
            'நெடுநல்வாடை': { ta: 'நெடுநல்வாடை நக்கீரரால் பாண்டியன் நெடுஞ்செழியனைப் பற்றிப் பாடப்பட்ட அகப்புற நூல்.', en: 'Nedunalvadai by Nakkeerar describes both the hero\'s valor and the heroine\'s separation.' },
            'மதுரைக்காஞ்சி': { ta: 'மதுரைக்காஞ்சி பத்துப்பாட்டில் மிக நீளமான நூல் (782 வரிகள்). இது மதுரையின் சிறப்புகளையும் வாழ்வின் நிலையாமையையும் கூறுகிறது.', en: 'Maduraikanchi is the longest (782 lines), describing Madurai city and the transience of life.' },
            'குறிஞ்சிப்பாட்டு': { ta: 'குறிஞ்சிப்பாட்டு கபிலரால் மலைநிலக் காதலைப் பற்றிப் பாடப்பட்டது. இதில் 99 வகையான மலர்கள் பட்டியலிடப்பட்டுள்ளன.', en: 'Kurinjippattu by Kapilar describes mountain love and lists 99 types of flowers.' },
            'பட்டினப்பாலை': { ta: 'பட்டினப்பாலை பூம்புகார் நகரத்தின் சிறப்பையும் கரிகாலனின் வீரத்தையும் விவரிக்கிறது.', en: 'Pattinappalai describes the port city of Puhar and the bravery of Karikal Chola.' },
            'மலைபடுகடாம்': { ta: 'மலைபடுகடாம் (கூத்தராற்றுப்படை) மலையில் தோன்றும் ஓசைகளை யானையின் மதத்திற்கு ஒப்பிட்டு விவரிக்கும் நூல்.', en: 'Malaipadukadam describes mountain echoes and the generosity of King Nannan.' }
        };

        // Check for book names
        for (let key in bookMatches) {
            if (q.includes(key.toLowerCase()) || q.includes(key) || (q.includes('pattinappalai') && key === 'பட்டினப்பாலை')) {
                return language === 'ta' ? bookMatches[key].ta : bookMatches[key].en;
            }
        }

        // 2. Extra keywords...
        if (q.includes('hello') || q.includes('hi') || q.includes('வணக்கம்')) {
            return language === 'ta' ? 'வணக்கம்! நான் பத்துப்பாட்டு உதவி. எதைப் பற்றி அறிய விரும்புகிறீர்கள்?' : 'Hello! I am your Pathu Pattu assistant. What would you like to know?';
        }

        if (q.includes('pattinappalai') || q.includes('pattina')) {
            return language === 'ta' ? 'பட்டினப்பாலை கரிகால் சோழனைப் பற்றியும் புகார் நகரத்தைப் பற்றியும் பாடுகிறது.' : 'Pattinappalai is a beautiful poem about King Karikal Chola and the prosperous port city of Kaveripoompattinam.';
        }

        // Default
        return language === 'ta'
            ? 'பத்துப்பாட்டு என்பது பண்டைய தமிழின் பத்து சிறந்த இலக்கிய நூல்களின் தொகுப்பு. நீங்கள் ஏதாவது ஒரு குறிப்பிட்ட நூலைப் (உதாரணமாக: மதுரைக்காஞ்சி) பற்றி கேட்கலாமே?'
            : 'Pathu Pattu is a collection of ten classical Tamil works. Please ask about a specific book like Maduraikanchi or a poet like Kapilar.';
    }

    // Log interactions for learning
    logInteraction(question, answer, language) {
        const interaction = {
            timestamp: new Date().toISOString(),
            question: question,
            answer: answer,
            language: language,
            helpful: null // Will be updated by user feedback
        };

        this.conversationHistory.push(interaction);

        // Save to localStorage for persistence
        this.saveToStorage();
    }

    // Add user feedback
    addFeedback(interactionIndex, wasHelpful, comment = '') {
        if (this.conversationHistory[interactionIndex]) {
            this.conversationHistory[interactionIndex].helpful = wasHelpful;
            this.conversationHistory[interactionIndex].comment = comment;

            this.feedbackData.push({
                timestamp: new Date().toISOString(),
                question: this.conversationHistory[interactionIndex].question,
                helpful: wasHelpful,
                comment: comment
            });

            this.saveToStorage();
        }
    }

    // Save to localStorage
    saveToStorage() {
        try {
            localStorage.setItem('pathuPattuConversations',
                JSON.stringify(this.conversationHistory));
            localStorage.setItem('pathuPattuFeedback',
                JSON.stringify(this.feedbackData));
        } catch (e) {
            console.warn('Could not save to localStorage:', e);
        }
    }

    // Load from localStorage
    loadFromStorage() {
        try {
            const conversations = localStorage.getItem('pathuPattuConversations');
            const feedback = localStorage.getItem('pathuPattuFeedback');

            if (conversations) {
                this.conversationHistory = JSON.parse(conversations);
            }
            if (feedback) {
                this.feedbackData = JSON.parse(feedback);
            }
        } catch (e) {
            console.warn('Could not load from localStorage:', e);
        }
    }

    // Export data for training
    exportTrainingData() {
        const helpfulInteractions = this.conversationHistory.filter(
            i => i.helpful === true
        );

        return {
            totalInteractions: this.conversationHistory.length,
            helpfulInteractions: helpfulInteractions.length,
            data: helpfulInteractions.map(i => ({
                question: i.question,
                answer: i.answer,
                language: i.language
            }))
        };
    }

    // Get analytics
    getAnalytics() {
        const total = this.conversationHistory.length;
        const helpful = this.conversationHistory.filter(i => i.helpful === true).length;
        const notHelpful = this.conversationHistory.filter(i => i.helpful === false).length;

        // Most common questions
        const questionFreq = {};
        this.conversationHistory.forEach(i => {
            const q = i.question.toLowerCase();
            questionFreq[q] = (questionFreq[q] || 0) + 1;
        });

        const topQuestions = Object.entries(questionFreq)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        return {
            totalQuestions: total,
            helpfulAnswers: helpful,
            notHelpfulAnswers: notHelpful,
            satisfactionRate: total > 0 ? (helpful / total * 100).toFixed(1) + '%' : 'N/A',
            topQuestions: topQuestions
        };
    }
}

// ==============================================
// INTEGRATION WITH EXISTING CHATBOT
// ==============================================

// Initialize AI
const pathuPattuAI = new PathuPattuAI();
pathuPattuAI.loadFromStorage();

// Replace the existing sendMessage function in app.js
async function sendMessageAI() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Display user message
    displayMessage(message, 'user');
    input.value = '';

    // Show typing indicator
    showTypingIndicator();

    try {
        // Get AI response (now an object with answer, engine, pages)
        const result = await pathuPattuAI.ask(message, currentLang);

        // Hide typing indicator
        hideTypingIndicator();

        // Build a rich response with scholarly metadata
        let enrichedAnswer = result.answer;

        if (result.pages && result.pages.length > 0) {
            const pagesTitle = currentLang === 'ta' ? 'ஆதாரம் (பக்கங்கள்)' : 'Source Pages';
            enrichedAnswer += `\n\n--- \n**${pagesTitle}:** ${result.pages.join(', ')}`;
        }

        if (result.engine) {
            enrichedAnswer += `\n\n<small style="opacity: 0.6; font-style: italic;">Engine: ${result.engine}</small>`;
        }

        // Display AI response
        displayMessage(enrichedAnswer, 'bot');

        // Show feedback buttons
        showFeedbackButtons(pathuPattuAI.conversationHistory.length - 1);

    } catch (error) {
        console.error('Chat Application Error:', error);
        hideTypingIndicator();
        displayMessage(
            currentLang === 'ta'
                ? 'மன்னிக்கவும், ஒரு பிழை ஏற்பட்டது. தயவுசெய்து உங்கள் இணைய இணைப்பைச் சரிபார்க்கவும்.'
                : 'Sorry, an error occurred. Please check your internet connection or console for details.',
            'bot'
        );
    }
}

// Note: UI functions (showTypingIndicator, hideTypingIndicator, scrollToBottom) 
// are now handled by the main app.js to avoid duplication.


// Feedback buttons
function showFeedbackButtons(interactionIndex) {
    const feedbackHTML = `
        <div class="feedback-buttons" id="feedback-${interactionIndex}">
            <p style="font-size: 0.85rem; color: #666; margin: 0.5rem 0;">
                ${currentLang === 'ta' ? 'இந்த பதில் உதவியாக இருந்ததா?' : 'Was this answer helpful?'}
            </p>
            <button onclick="provideFeedback(${interactionIndex}, true)" class="feedback-btn helpful">
                👍 ${currentLang === 'ta' ? 'ஆம்' : 'Yes'}
            </button>
            <button onclick="provideFeedback(${interactionIndex}, false)" class="feedback-btn not-helpful">
                👎 ${currentLang === 'ta' ? 'இல்லை' : 'No'}
            </button>
        </div>
    `;

    const messagesContainer = document.getElementById('chatMessages');
    const feedbackDiv = document.createElement('div');
    feedbackDiv.innerHTML = feedbackHTML;
    messagesContainer.appendChild(feedbackDiv.firstElementChild);
    scrollToBottom();
}

function provideFeedback(interactionIndex, wasHelpful) {
    pathuPattuAI.addFeedback(interactionIndex, wasHelpful);

    // Remove feedback buttons
    const feedbackDiv = document.getElementById(`feedback-${interactionIndex}`);
    if (feedbackDiv) {
        feedbackDiv.innerHTML = `
            <p style="font-size: 0.85rem; color: #4CAF50; margin: 0.5rem 0;">
                ${currentLang === 'ta' ? 'நன்றி! உங்கள் கருத்து பதிவு செய்யப்பட்டது.' : 'Thank you! Your feedback has been recorded.'}
            </p>
        `;
    }

    console.log('Analytics:', pathuPattuAI.getAnalytics());
}

// Note: scrollToBottom is handled by displayMessage in app.js


// ==============================================
// ADMIN FUNCTIONS (for you to monitor)
// ==============================================

// View analytics in console
function viewAnalytics() {
    console.log('=== PATHU PATTU AI ANALYTICS ===');
    console.log(pathuPattuAI.getAnalytics());
}

// Export training data
function exportData() {
    const data = pathuPattuAI.exportTrainingData();
    console.log('=== TRAINING DATA ===');
    console.log(JSON.stringify(data, null, 2));

    // Download as JSON file
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pathu-pattu-training-data.json';
    a.click();
}

// Clear all data
function clearAllData() {
    if (confirm('Clear all conversation data?')) {
        localStorage.removeItem('pathuPattuConversations');
        localStorage.removeItem('pathuPattuFeedback');
        pathuPattuAI.conversationHistory = [];
        pathuPattuAI.feedbackData = [];
        console.log('All data cleared');
    }
}

// ==============================================
// USAGE INSTRUCTIONS
// ==============================================

console.log(`
🤖 PATHU PATTU AI SCHOLAR READY!

ARCHITECTURE:
✅ Advanced RAG (Retrieval-Augmented Generation)
✅ Primary Brain: OpenAI GPT-4o-mini
✅ 814 Pages of Library Knowledge Base
✅ Automatic Language Detection

ADMIN COMMANDS (in browser console):
- viewAnalytics()     - See usage statistics
- exportData()        - Download interaction data
- clearAllData()      - Clear local session data

The AI Scholar is now securely connected to the production backend.
API keys are managed safely in the cloud (no longer exposed in browser).
`);
