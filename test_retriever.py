
from backend.retriever import retrieve_legal_context

question = """
I purchased a damaged mobile phone from Amazon.
The seller refused to refund my money.
What are the obligations of the marketplace seller
and what refund rights may apply?
"""

results = retrieve_legal_context(question, k=8)

for i, doc in enumerate(results, start=1):
    print(f"\nRESULT {i}")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("Content:", doc.page_content[:800])
