const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Chat Endpoint (Connected to Python RAG Model)
app.post('/api/chat', async (req, res) => {
    try {
        const { message, language } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log(`📡 Querying RAG Model (Port 5000) for: "${message.substring(0, 50)}..."`);

        // Call the Python RAG Server
        const response = await fetch(`http://localhost:5000/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: message,
                language: language || 'en'
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('RAG Model Error:', data);
            return res.status(response.status).json({
                error: 'RAG Model Error',
                details: data
            });
        }

        // Return the synthesized answer to the frontend
        res.json({
            answer: data.answer,
            pages: data.pages,
            engine: data.engine
        });

    } catch (error) {
        console.error('Server Internal Error (Check if Python server is running on 5000):', error);
        res.status(500).json({
            error: 'AI Server Offline',
            message: 'My advanced knowledge base is currently initializing. Please try again in 30 seconds.'
        });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Pathu Pattu AI Server running at http://localhost:${PORT}`);
    console.log(`🔒 API Key secured in backend`);
});
