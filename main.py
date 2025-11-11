from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import os

from utils.pdf_utils import extract_text_from_pdf


app = FastAPI(title="RAG Chatbot with Groq")


UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message":"RAG Chatbot API is running!"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, "f{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    pages = extract_text_from_pdf(file_path)
    return {"document_id": file_id, "pages_extracted": len(pages)}
