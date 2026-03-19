const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
    origin: '*', // Allows all origins (including Vercel)
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());
app.use(express.static('./')); // Serve the website files

// Chat Endpoint (Connected to Python RAG Model)
app.post('/api/chat', async (req, res) => {
    try {
        const { message, language, history } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`📡 Querying RAG Model for: "${message.substring(0, 50)}..."`);

        // Check if Python server is up with a longer timeout for AI thinking
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 45000); // Increased to 45 seconds for complex Tamil responses

        try {
            const response = await fetch(`http://localhost:5000/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: message,
                    language: language || 'en',
                    history: history || []
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'RAG Error');

            res.json({
                answer: data.answer,
                pages: data.pages,
                engine: data.engine
            });

        } catch (fetchError) {
            clearTimeout(timeoutId);
            console.warn('AI Brain not ready yet:', fetchError.message);

            // If it's a connection error or timeout, return "Initializing" status
            res.status(503).json({
                error: 'AI_INITIALIZING',
                message: 'Pattu LLM is currently loading its massive library. This happens once after a period of inactivity. Please try again in 15 seconds.',
                engine: 'Loading...'
            });
        }

    } catch (error) {
        console.error('Server Internal Error:', error);
        res.status(500).json({
            error: 'Server Error',
            message: 'An unexpected error occurred. Please refresh the page.'
        });
    }
});

// ---- Keep-Alive Logic for Render Free Tier ----
const WAKE_UP_URL = process.env.WAKE_UP_URL || 'https://patthu-pattu.onrender.com/';

function keepAlive() {
    console.log('⏰ Keep-Alive: Pinging server to prevent sleep...');
    try {
        fetch(WAKE_UP_URL)
            .then(res => console.log(`⏰ Keep-Alive: Ping successful (${res.status})`))
            .catch(err => console.error('⏰ Keep-Alive: Ping failed', err.message));
    } catch (e) {
        console.error('⏰ Keep-Alive Error:', e.message);
    }
}

app.listen(PORT, () => {
    console.log(`🚀 Pathu Pattu AI Server running at http://localhost:${PORT}`);
    console.log(`🔒 API Key secured in backend`);

    // Ping ourselves every 10 minutes (600,000 milliseconds)
    setInterval(keepAlive, 10 * 60 * 1000);
});
