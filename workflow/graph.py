from langgraph.graph import StateGraph, START, END

from agents.schemas import NyayaState

from agents.intake import intake_agent
from agents.classifier import classifier_agent
from agents.legal_researcher import legal_researcher_agent
from agents.legal_advisor import legal_advisor_agent
from agents.verifier import verifier_agent
from agents.document_generator import document_generator_agent


def build_graph():

    # Create graph
    builder = StateGraph(NyayaState)

    # Register agents as nodes
    builder.add_node("intake", intake_agent)
    builder.add_node("classifier", classifier_agent)
    builder.add_node("researcher", legal_researcher_agent)
    builder.add_node("advisor", legal_advisor_agent)
    builder.add_node("verifier", verifier_agent)
    builder.add_node("document_generator", document_generator_agent)

    # Define execution sequence
    builder.add_edge(START, "intake")
    builder.add_edge("intake", "classifier")
    builder.add_edge("classifier", "researcher")
    builder.add_edge("researcher", "advisor")
    builder.add_edge("advisor", "verifier")
    builder.add_edge("verifier", "document_generator")
    builder.add_edge("document_generator", END)

    # Compile graph
    graph = builder.compile()

    return graph