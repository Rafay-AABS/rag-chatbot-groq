import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("pdf_docs")

embedding_fn = embedding_functions.DefaultEmbeddingFunction()

def store_chunks(document_id, chunks):
    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=[{"document_id": document_id} for _ in chunks]
    )
    return len(chunks)
