
import time

from agents.intake import intake_agent
from agents.classifier import classifier_agent
from agents.legal_researcher import legal_researcher_agent
from agents.legal_advisor import legal_advisor_agent
from agents.verifier import verifier_agent
from agents.document_generator import document_generator_agent


state = {
    "user_query": """
    I purchased a Samsung Galaxy smartphone for Rs. 25000
    from Amazon on 15 October 2026.
    It arrived with a cracked screen.
    The seller refused a refund or replacement.
    I contacted Amazon customer support.
    I have the invoice and photographs.
    """
}


def run_agent(name, agent, state):

    print(f"\nRunning {name}...")
    start = time.perf_counter()

    result = agent(state)
    state.update(result)

    elapsed = time.perf_counter() - start

    print(f"{name} completed in {elapsed:.2f} seconds")

    return state


total_start = time.perf_counter()

run_agent("Intake", intake_agent, state)
run_agent("Classifier", classifier_agent, state)
run_agent("Legal Researcher", legal_researcher_agent, state)
run_agent("Legal Advisor", legal_advisor_agent, state)
run_agent("Verifier", verifier_agent, state)

# Test document generation separately
run_agent("Document Generator", document_generator_agent, state)

print("\nTotal execution time:",
      round(time.perf_counter() - total_start, 2),
      "seconds")
