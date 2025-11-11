import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str):
    text_pages = []
    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            text_pages.append({"page": page_num, "text": text})
    return text_pages