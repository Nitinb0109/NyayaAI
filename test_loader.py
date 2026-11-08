
from backend.document_loader import load_legal_documents

documents = load_legal_documents()

for doc in documents:
    if doc.metadata["source"] == "ecommerce_rules.pdf":
        print("\n" + "=" * 60)
        print("PAGE:", doc.metadata["page"])
        print(doc.page_content[:1000])

