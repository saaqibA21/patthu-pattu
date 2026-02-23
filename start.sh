#!/bin/bash
# Start the Python AI Brain in the background
echo "🤖 Starting Python AI Brain (In Background)..."
python smart_model_server.py &

# Start the Node.js Web Server IMMEDIATELY
# This makes Render happy as it detects the port binding quickly
echo "🚀 Starting Node.js Web Server..."
node server.js
