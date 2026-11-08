from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(
        "data/vectorstore/consumer_law_faiss"
    )

    print("Vector store created successfully!")

    return vector_store