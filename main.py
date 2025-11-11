import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.pdf_utils import extract_text_from_pdf, chunk_text
from utils.embedding_utils import store_chunks


app = FastAPI(title="RAG Chatbot with Groq")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    pages = extract_text_from_pdf(file_path)
    if not pages:
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF.")

    # Combine and chunk text
    all_text = " ".join([p["text"] for p in pages if "text" in p])
    chunks = chunk_text(all_text)

    # Store chunks (e.g., in a vector DB or embedding store)
    stored_count = store_chunks(file_id, chunks)

    return {
        "document_id": file_id,
        "pages_extracted": len(pages),
        "chunks_created": len(chunks),
        "chunks_stored": stored_count
    }