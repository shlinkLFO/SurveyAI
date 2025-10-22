#!/bin/bash
# Start script for AI Confidence Survey

echo "Starting AI Confidence Survey..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

