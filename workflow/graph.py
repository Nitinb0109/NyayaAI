
from langgraph.graph import StateGraph, START, END

from agents.schemas import NyayaState

from agents.intake import intake_agent
from agents.classifier import classifier_agent
from agents.legal_researcher import legal_researcher_agent
from agents.legal_advisor import legal_advisor_agent
from agents.verifier import verifier_agent
from agents.document_generator import document_generator_agent


# Decide whether the question is within NyayaAI's scope
def scope_check(state: NyayaState):

    category = state.get("issue_category", "OTHER")

    if category == "OUT_OF_SCOPE":
        return "out_of_scope"

    return "researcher"


# Handle unrelated questions
def out_of_scope_agent(state: NyayaState):

    return {
        "final_response": (
            "I am NyayaAI, an AI assistant designed specifically "
            "to help with Indian consumer disputes.\n\n"

            "I can help you with:\n"
            "- Defective or damaged products\n"
            "- Refund and replacement issues\n"
            "- Counterfeit or fake products\n"
            "- Misleading advertisements\n"
            "- Delivery and e-commerce complaints\n"
            "- Unresolved consumer grievances\n\n"

            "Your question does not appear to be related to "
            "a consumer dispute. Please describe your consumer-related "
            "problem so I can assist you."
        ),
        "legal_answer": "",
        "generated_document": "",
        "verification_result": ""
    }


def build_graph():

    builder = StateGraph(NyayaState)

    # Register agents
    builder.add_node("intake", intake_agent)
    builder.add_node("classifier", classifier_agent)
    builder.add_node("out_of_scope", out_of_scope_agent)
    builder.add_node("researcher", legal_researcher_agent)
    builder.add_node("advisor", legal_advisor_agent)
    builder.add_node("verifier", verifier_agent)
    builder.add_node("document_generator", document_generator_agent)

    # Initial workflow
    builder.add_edge(START, "intake")
    builder.add_edge("intake", "classifier")

    # Conditional routing after classification
    builder.add_conditional_edges(
        "classifier",
        scope_check,
        {
            "researcher": "researcher",
            "out_of_scope": "out_of_scope"
        }
    )

    # Legal RAG workflow
    builder.add_edge("researcher", "advisor")
    builder.add_edge("advisor", "verifier")
    builder.add_edge("verifier", "document_generator")
    builder.add_edge("document_generator", END)

    # Stop after rejecting unrelated questions
    builder.add_edge("out_of_scope", END)

    return builder.compile()
