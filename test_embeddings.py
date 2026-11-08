from backend.document_loader import load_legal_documents
from backend.chunking import create_chunks
from backend.embeddings import create_vector_store

# Step 1: Load legal PDFs
documents = load_legal_documents()

# Step 2: Split documents into chunks
chunks = create_chunks(documents)

# Step 3: Generate embeddings and create FAISS database
vector_store = create_vector_store(chunks)

print("\nEmbedding and vector database creation completed!")