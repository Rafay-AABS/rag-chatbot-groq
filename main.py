import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from utils.pdf_utils import PDFProcessor
from utils.embedding_utils import EmbeddingStore
from utils.rag_pipeline import RAGPipeline
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Chatbot with Groq")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pdf_processor = PDFProcessor()
embedding_store = EmbeddingStore()
rag_pipeline = RAGPipeline()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    # Save the uploaded file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    pages = pdf_processor.extract_text_from_pdf(file_path)
    if not pages:
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")

    # Combine and chunk text
    all_text = " ".join([p["text"] for p in pages if "text" in p])
    chunks = pdf_processor.chunk_text(all_text)


    stored_count = embedding_store.store_chunks(file_id, chunks)

    return {
        "document_id": file_id,
        "pages_extracted": len(pages),
        "chunks_created": len(chunks),
        "chunks_stored": stored_count
    }

class ChatRequest(BaseModel):
    question: str
    document_id: str

@app.post("/chat")
async def chat_with_pdf(req: ChatRequest):
    answer, sources = rag_pipeline.ask_question(req.question, req.document_id)
    return {"answer": answer, "sources": sources}
