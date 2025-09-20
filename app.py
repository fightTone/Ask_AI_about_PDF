from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
import json
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store PDF content for chat context
pdf_content = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global pdf_content

    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from PDF
        pdf_content = extract_pdf_text(filepath)

        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'PDF uploaded successfully'
        })

    return jsonify({'error': 'Please upload a valid PDF file'}), 400

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat', methods=['POST'])
def chat():
    global pdf_content

    user_message = request.json.get('message', '')

    if not pdf_content:
        return jsonify({'error': 'No PDF loaded. Please upload a PDF first.'}), 400

    # Prepare context for Ollama
    context = f"Based on the following PDF content, please answer the user's question:\n\nPDF Content:\n{pdf_content[:4000]}...\n\nUser Question: {user_message}"

    try:
        # Call Ollama API
        ollama_response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': 'dolphin-llama3:latest',
                'prompt': context,
                'stream': False
            },
            timeout=30
        )

        if ollama_response.status_code == 200:
            response_data = ollama_response.json()
            return jsonify({'response': response_data['response']})
        else:
            return jsonify({'error': 'Failed to get response from Ollama'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Cannot connect to Ollama. Make sure Ollama is running.'}), 500

def extract_pdf_text(filepath):
    text = ""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text

if __name__ == '__main__':
    app.run(debug=True)