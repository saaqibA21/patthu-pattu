#!/bin/bash
# Start the Python AI Brain in the background
python smart_model_server.py &

# Start the Node.js Web Server
node server.js
