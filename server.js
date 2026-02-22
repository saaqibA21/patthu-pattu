const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Gemini API Configuration
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

// Chat Endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message, context, language } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        if (!GEMINI_API_KEY || GEMINI_API_KEY === 'YOUR_GEMINI_API_KEY_HERE') {
            return res.status(500).json({ error: 'Gemini API Key not configured' });
        }

        // Build prompt
        const prompt = `${context}\n\nUser Question (${language === 'ta' ? 'Tamil' : 'English'}): ${message}`;

        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    maxOutputTokens: 1024,
                }
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Gemini API Error details:', JSON.stringify(data, null, 2));
            return res.status(response.status).json(data);
        }

        // Extract answer from Gemini format
        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            const answer = data.candidates[0].content.parts[0].text;
            res.json({ answer: answer });
        } else {
            res.status(500).json({ error: 'Unexpected response format from Google' });
        }

    } catch (error) {
        console.error('Server Internal Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Pathu Pattu AI Server running at http://localhost:${PORT}`);
    console.log(`🔒 API Key secured in backend`);
});
