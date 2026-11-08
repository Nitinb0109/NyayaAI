
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1800,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    # Add a unique index to each chunk
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    print(f"Total chunks created: {len(chunks)}")

    return chunks
