
from backend.retriever import retrieve_legal_context


def legal_researcher_agent(state):

    facts = state["extracted_facts"]
    category = state["issue_category"]

    issue = facts.get("issue") or ""
    seller_response = facts.get("seller_response") or ""
    product = facts.get("product") or ""

    # Build a dispute-specific retrieval query
    query = f"""
    Indian consumer protection law.

    Dispute category: {category}
    Product: {product}
    Consumer issue: {issue}
    Seller response: {seller_response}

    Find relevant provisions concerning:
    - Consumer rights and remedies
    - Defective or damaged goods
    - Refund and replacement obligations
    - E-commerce marketplace seller duties
    - E-commerce grievance redressal
    - Relevant sections of Consumer Protection Act 2019
    - Relevant rules of Consumer Protection E-Commerce Rules 2020

    Retrieve exact legal text with source and page information.
    """

    # Retrieve relevant legal documents
    documents = retrieve_legal_context(query, k=8)

    retrieved_context = []

    for doc in documents:

        retrieved_context.append({
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "content": doc.page_content
        })

    print("\nLEGAL RESEARCH COMPLETED")
    print("Issue category:", category)
    print("Documents retrieved:", len(retrieved_context))

    return {
        "retrieved_context": retrieved_context
    }
