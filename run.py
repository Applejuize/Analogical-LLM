#!/usr/bin/env python3
"""
Simple runner script to start the Flask server with proper error handling
"""
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'langchain', 'langgraph', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install flask flask-cors langchain langchain-community langchain-core langchain-openai langgraph openai python-dotenv")
        return False
    
    return True

def check_api_key():
    """Check if OpenAI API key is set"""
    if not os.environ.get('OPENAI_API_KEY'):
        print("OPENAI_API_KEY environment variable is not set.")
        print("Please set it using: export OPENAI_API_KEY='your-api-key-here'")
        return False
    return True

if __name__ == '__main__':
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("Checking API key...")
    if not check_api_key():
        sys.exit(1)
    
    print("Starting server...")
    try:
        from server import app
        app.run(debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)