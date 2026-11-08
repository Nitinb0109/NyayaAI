from backend.retriever import retrieve_legal_context
from backend.llm import generate_legal_answer

question = "What can I do if an online seller refuses to refund my money?"

# Retrieve relevant legal chunks
documents = retrieve_legal_context(question, k=4)

# Combine retrieved content with source information
context = ""

for doc in documents:
    context += f"""
    Source: {doc.metadata['source']}
    Page: {doc.metadata['page']}

    Content:
    {doc.page_content}

    -------------------------
    """

# Generate answer using Gemini
answer = generate_legal_answer(question, context)

print("\n========== NYAYAAI RESPONSE ==========\n")
print(answer)