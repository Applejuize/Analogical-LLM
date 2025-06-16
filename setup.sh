#!/bin/bash
# Setup script for the Analogical-LLM project

echo "Setting up Analogical-LLM project..."

# Ensure pip is available
echo "Ensuring pip is available..."
python3 -m ensurepip --upgrade

# Install required packages
echo "Installing required packages..."
pip install flask flask-cors langchain langchain-community langchain-core langchain-openai langgraph openai python-dotenv

echo "Setup complete!"
echo ""
echo "To run the server:"
echo "1. Set your OpenAI API key: export OPENAI_API_KEY='your-api-key-here'"
echo "2. Run: python3 run.py"