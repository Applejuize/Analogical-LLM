from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from main import process_query

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/process', methods=['POST'])
def process_user_query():
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Process the query through the analogical reasoning pipeline
        result = process_query(user_query)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your query. Please try again.'
        }), 500

if __name__ == '__main__':
    # Set OpenAI API key if not already set
    if not os.environ.get('OPENAI_API_KEY'):
        print("Please set your OPENAI_API_KEY environment variable")
        exit(1)
    
    app.run(debug=True, port=5000)