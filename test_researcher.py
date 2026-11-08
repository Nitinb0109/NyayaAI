
from agents.legal_researcher import legal_researcher_agent

state = {
    "issue_category": "DEFECTIVE_PRODUCT",

    "extracted_facts": {
        "product": "Samsung mobile phone",
        "issue": "Phone arrived with a damaged screen",
        "seller_response": "Seller refused to provide a refund"
    }
}

result = legal_researcher_agent(state)

for i, doc in enumerate(result["retrieved_context"], start=1):

    print(f"\nRESULT {i}")
    print("Source:", doc["source"])
    print("Page:", doc["page"])
    print("Content:", doc["content"][:1000])
