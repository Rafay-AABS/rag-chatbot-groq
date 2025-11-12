from utils.embedding_utils import EmbeddingStore
import os
from groq import Groq

class RAGPipeline:
    def __init__(self):
        self.embedding_store = EmbeddingStore()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def ask_question(self, question: str, document_id: str, top_k=3):
        # Embed the question
        query_vector = self.embedding_store.embedding_fn([question])
        
        # Retrieve top chunks safely
        results = self.embedding_store.collection.query(
            query_embeddings=query_vector,
            n_results=top_k,
            where={"document_id": document_id}
        )
        
        # Handle empty retrieval
        if not results or not results.get("documents") or not results["documents"][0]:
            print(f"DEBUG: No chunks found for document_id={document_id}")
            return "No context found for this document.", []
        
        chunks = results["documents"][0]
        print(f"DEBUG: Retrieved {len(chunks)} chunks for doc_id={document_id}")
        
        # Build prompt
        contexts = "\n\n".join(chunks)
        prompt = f"Use the following context to answer the question.\n\nContext:\n{contexts}\n\nQuestion: {question}\nAnswer:"
        
        # Call Groq LLM safely
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
        except Exception as e:
            print(f"DEBUG: Groq API call failed: {e}")
            return "Error calling LLM. Check API key, model, and network.", chunks
        
        return answer, chunks
