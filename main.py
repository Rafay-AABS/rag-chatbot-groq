from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message":"RAG Chatbot API is running!"}