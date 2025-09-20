# PDF Chat Assistant

A Flask web application that allows users to upload PDFs and chat about them using Ollama's dolphin-llama3 model.

## Features

- 📄 PDF upload via drag & drop or file picker
- 👁️ Built-in PDF viewer
- 💬 AI-powered chat about PDF content
- 🐬 Powered by Ollama's dolphin-llama3:latest model

## Prerequisites

1. **Python 3.7+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **dolphin-llama3 model** - Pull with: `ollama pull dolphin-llama3:latest`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Verify the model is available:
```bash
ollama list
```

## Usage

1. Start the Flask app:
```bash
python app.py
```

2. Open your browser to `http://localhost:5000`

3. Upload a PDF file using drag & drop or the file picker

4. Start chatting about the PDF content in the right sidebar!

## How it works

- PDFs are uploaded to the `uploads/` directory
- Text is extracted using PyPDF2
- The extracted text serves as context for Ollama
- User questions are sent to dolphin-llama3:latest with PDF context
- Responses are displayed in real-time chat interface

## File Structure

```
PDF_works/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Frontend interface
├── uploads/            # PDF storage (created automatically)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```