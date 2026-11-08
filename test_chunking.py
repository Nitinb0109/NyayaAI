
from backend.document_loader import load_legal_documents
from backend.chunking import create_chunks

# Load legal documents
documents = load_legal_documents()

# Create smaller chunks
chunks = create_chunks(documents)

# Inspect first five chunks
for chunk in chunks[:5]:

    print("\n" + "=" * 70)

    print("Source:", chunk.metadata["source"])
    print("Page:", chunk.metadata["page"])
    print("Chunk ID:", chunk.metadata["chunk_id"])

    print(chunk.page_content[:500])
