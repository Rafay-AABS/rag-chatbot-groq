# 🤖 RAG Chatbot with Groq

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful **Retrieval-Augmented Generation (RAG)** chatbot that enables intelligent conversations with your PDF documents. Built with FastAPI, ChromaDB, and Groq's lightning-fast LLM inference, this application extracts context from PDFs and provides accurate, source-backed answers to your questions.

## ✨ Features

- 📄 **PDF Document Upload** - Upload and process PDF files
- 🔍 **Intelligent Text Extraction** - Extracts and chunks text from PDFs using PyMuPDF
- 🧠 **Vector Embeddings** - Stores document chunks as embeddings in ChromaDB
- ⚡ **Lightning-Fast Responses** - Powered by Groq's high-performance LLM (Llama 3.1)
- 🎯 **Context-Aware Answers** - Retrieves relevant document chunks before generating responses
- 🔗 **Source Citations** - Returns the source chunks used to generate each answer
- 🚀 **RESTful API** - Easy-to-use FastAPI endpoints for integration

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   PDF File  │─────▶│ Text Extract │─────▶│  Chunking   │
└─────────────┘      └──────────────┘      └─────────────┘
                                                   │
                                                   ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Answer    │◀─────│   Groq LLM   │◀─────│  ChromaDB   │
└─────────────┘      └──────────────┘      └─────────────┘
                            ▲                      ▲
                            │                      │
                     ┌──────┴──────────────────────┘
                     │     Context Retrieval
                     │
              ┌──────┴──────┐
              │   Question  │
              └─────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- A Groq API key ([Get one here](https://console.groq.com/))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Rafay-AABS/rag-chatbot-groq.git
cd rag-chatbot-groq
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Endpoints

#### 1. Upload PDF Document

**POST** `/upload`

Upload a PDF file to be processed and stored.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

**Response:**
```json
{
  "document_id": "uuid-string",
  "pages_extracted": 10,
  "chunks_created": 45,
  "chunks_stored": 45
}
```

#### 2. Ask Questions

**POST** `/chat`

Ask questions about an uploaded document.

**Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of the document?",
    "document_id": "uuid-from-upload"
  }'
```

**Response:**
```json
{
  "answer": "The main topic of the document is...",
  "sources": [
    "chunk of text 1...",
    "chunk of text 2...",
    "chunk of text 3..."
  ]
}
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Web Framework** | FastAPI |
| **LLM Provider** | Groq (Llama 3.1) |
| **Vector Database** | ChromaDB |
| **PDF Processing** | PyMuPDF (fitz) |
| **Embeddings** | Sentence Transformers |
| **Language** | Python 3.8+ |

## 📁 Project Structure

```
rag-chatbot-groq/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── README.md              # Project documentation
├── data/
│   ├── uploads/           # Uploaded PDF files storage
│   └── chroma_db/         # ChromaDB vector database
└── utils/
    ├── pdf_utils.py       # PDF text extraction and chunking
    ├── embedding_utils.py # Vector embedding and storage
    └── rag_pipeline.py    # RAG query and response generation
```

## ⚙️ Configuration

### Chunking Parameters

Modify in `utils/pdf_utils.py`:

```python
def chunk_text(text: str, max_length=1000, overlap=100):
    # max_length: Maximum characters per chunk
    # overlap: Overlapping characters between chunks
```

### Retrieval Settings

Modify in `utils/rag_pipeline.py`:

```python
def ask_question(question: str, document_id: str, top_k=3):
    # top_k: Number of relevant chunks to retrieve
```

### LLM Model

Change the Groq model in `utils/rag_pipeline.py`:

```python
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # Change model here
    messages=[{"role": "user", "content": prompt}]
)
```

Available models: `llama-3.1-8b-instant`, `llama-3.1-70b-versatile`, `mixtral-8x7b-32768`, etc.

## 🔧 Advanced Usage

### Using with Python Requests

```python
import requests

# Upload PDF
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload",
        files={"file": f}
    )
    doc_id = response.json()["document_id"]

# Ask question
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "question": "What are the key findings?",
        "document_id": doc_id
    }
)
print(response.json()["answer"])
```

## 🐛 Troubleshooting

### No context found for document
- Ensure the document_id from upload matches the one used in chat
- Check that the PDF contains extractable text (not just images)

### Groq API errors
- Verify your API key in `.env`
- Check your API rate limits on Groq console
- Ensure you have internet connectivity

### ChromaDB errors
- Delete the `data/chroma_db` folder and restart
- Ensure sufficient disk space

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing ultra-fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing

## 📧 Contact

**Rafay AABS** - [GitHub](https://github.com/Rafay-AABS)

Project Link: [https://github.com/Rafay-AABS/rag-chatbot-groq](https://github.com/Rafay-AABS/rag-chatbot-groq)

---

⭐ If you find this project helpful, please give it a star!

---