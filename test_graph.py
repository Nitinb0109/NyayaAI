from workflow.graph import build_graph


# Build LangGraph workflow
graph = build_graph()


# User complaint
initial_state = {
    "user_query": """
    I purchased a Samsung mobile phone for Rs. 20000
    from Amazon on 10 October 2026.

    The phone arrived with a damaged screen.
    The seller refused to provide a refund.

    I have the invoice and photographs.
    """
}


# Execute complete workflow
result = graph.invoke(initial_state)


print("\n========== NYAYAAI FINAL OUTPUT ==========\n")

print("ISSUE CATEGORY:")
print(result["issue_category"])

print("\nLEGAL ADVICE:")
print(result["legal_answer"])

print("\nVERIFICATION:")
print(result["verification_result"])

print("\nGENERATED COMPLAINT:")
print(result["generated_document"])