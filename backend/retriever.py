
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from functools import lru_cache

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = "data/vectorstore/consumer_law_faiss"

# Load embedding model and FAISS database
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


# Create hybrid retriever
@lru_cache(maxsize=1)
def create_hybrid_retriever():
    vector_store = load_vector_store()

    # Semantic retriever
    semantic_retriever = vector_store.as_retriever(
        search_kwargs={"k": 8}
    )

    # Keyword retriever
    all_documents = list(
        vector_store.docstore._dict.values()
    )

    keyword_retriever = BM25Retriever.from_documents(
        all_documents
    )
    keyword_retriever.k = 8

    return semantic_retriever, keyword_retriever


def retrieve_legal_context(question, k=5):
    semantic_retriever, keyword_retriever = (
        create_hybrid_retriever()
    )

    semantic_results = semantic_retriever.invoke(question)
    keyword_results = keyword_retriever.invoke(question)

    # Merge results and remove duplicate chunks
    combined_results = []
    seen = set()

    for doc in semantic_results + keyword_results:
        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.page_content
        )

        if key not in seen:
            seen.add(key)
            combined_results.append(doc)

    return combined_results[:k]
