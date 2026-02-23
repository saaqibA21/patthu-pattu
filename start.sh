#!/bin/bash
# Start the Python AI Brain in the background
echo "🤖 Starting Python AI Brain..."
python smart_model_server.py &

# Wait for Port 5000 to be ready (up to 60 seconds)
echo "⏳ Waiting for AI Brain to initialize..."
for i in {1..60}; do
    if curl -s http://localhost:5000 > /dev/null; then
        echo "✅ AI Brain is ready!"
        break
    fi
    sleep 1
done

# Start the Node.js Web Server
echo "🚀 Starting Node.js Web Server..."
node server.js
