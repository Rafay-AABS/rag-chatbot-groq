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