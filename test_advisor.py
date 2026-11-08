
from agents.legal_researcher import legal_researcher_agent
from agents.legal_advisor import legal_advisor_agent

state = {
    "issue_category": "DEFECTIVE_PRODUCT",
    "extracted_facts": {
        "product": "Samsung mobile phone",
        "purchase_amount": 20000,
        "issue": "Phone arrived with a damaged screen",
        "seller_response": "Seller refused to provide a refund",
        "evidence": ["Invoice", "Photographs"]
    }
}

# First retrieve legal provisions
research_result = legal_researcher_agent(state)
state.update(research_result)

# Then generate legal explanation
advisor_result = legal_advisor_agent(state)

print("\nLEGAL ADVICE:\n")
print(advisor_result["legal_answer"])
