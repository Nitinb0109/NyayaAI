from agents.intake import intake_agent
from agents.classifier import classifier_agent

state = {
    "user_query": """
    I purchased a Samsung phone for Rs. 20000.
    It arrived with a damaged screen.
    The seller refused my refund.
    I have the invoice and photographs.
    """
}

# First agent
intake_result = intake_agent(state)
state.update(intake_result)

# Second agent
classification_result = classifier_agent(state)

print("\n========== CLASSIFICATION OUTPUT ==========")
print(classification_result)