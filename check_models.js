const dotenv = require('dotenv');
dotenv.config();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

async function checkModels() {
    console.log('Checking available models for your API key...');
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}`);
        const data = await response.json();

        if (data.models) {
            console.log('\n✅ Models available to you:');
            data.models.forEach(m => {
                if (m.supportedGenerationMethods.includes('generateContent')) {
                    console.log(`- ${m.name}`);
                }
            });
        } else {
            console.error('\n❌ Could not list models:', data);
        }
    } catch (error) {
        console.error('\n❌ Error connecting to Google:', error.message);
    }
}

checkModels();
