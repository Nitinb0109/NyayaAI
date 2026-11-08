
import pickle
from functools import lru_cache
from pathlib import Path

from langchain_community.retrievers import BM25Retriever

VECTOR_DB_PATH = Path("data/vectorstore/consumer_law_faiss")


@lru_cache(maxsize=1)
def create_retriever():

    print("Loading legal documents...")

    # Load the existing FAISS metadata file.
    # This is your own locally generated file.
    index_file = VECTOR_DB_PATH / "index.pkl"

    with open(index_file, "rb") as file:
        docstore, index_to_docstore_id = pickle.load(file)

    documents = list(docstore._dict.values())

    retriever = BM25Retriever.from_documents(documents)
    retriever.k = 5

    print(f"Loaded {len(documents)} legal chunks.")

    return retriever


def retrieve_legal_context(question, k=5):

    retriever = create_retriever()
    retriever.k = k

    return retriever.invoke(question)


