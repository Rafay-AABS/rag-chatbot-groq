from utils.embedding_utils import collection, embedding_fn
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_question(question: str, document_id: str, top_k=3):
    # Embed the question
    query_vector = embedding_fn([question])
    
    # Retrieve top chunks from Chroma
    results = collection.query(
        query_embeddings=query_vector,
        n_results=top_k,
        where={"document_id": document_id}
    )
    
    # Combine retrieved texts
    contexts = "\n\n".join(results["documents"][0])
    prompt = f"Use the following context to answer:\n{contexts}\n\nQuestion: {question}\nAnswer:"
    
    # Call Groq LLM
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    return answer, results["documents"][0]
