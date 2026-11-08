from agents.intake import intake_agent
from agents.classifier import classifier_agent
from agents.legal_researcher import legal_researcher_agent
from agents.legal_advisor import legal_advisor_agent
from agents.verifier import verifier_agent
from agents.document_generator import document_generator_agent


state = {
    "user_query": """
    I purchased a Samsung mobile phone for Rs. 20000
    from Amazon on 10 October 2026.

    The phone arrived with a damaged screen.
    The seller refused to provide a refund.

    I have the invoice and photographs.
    """
}

# Execute agents
state.update(intake_agent(state))
state.update(classifier_agent(state))
state.update(legal_researcher_agent(state))
state.update(legal_advisor_agent(state))
state.update(verifier_agent(state))

# Generate complaint
state.update(document_generator_agent(state))

print("\n========== GENERATED CONSUMER COMPLAINT ==========\n")
print(state["generated_document"])