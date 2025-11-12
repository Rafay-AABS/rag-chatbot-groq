import chromadb
from chromadb.utils import embedding_functions

class EmbeddingStore:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection("pdf_docs")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    def store_chunks(self, document_id, chunks):
        ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        self.collection.add(
            ids=ids,
            documents=chunks,
            metadatas=[{"document_id": document_id} for _ in chunks]
        )
        return len(chunks)
