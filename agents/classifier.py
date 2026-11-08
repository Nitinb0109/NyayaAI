
def classifier_agent(state):

    facts = state.get("extracted_facts", {})

    # Read the original user question too
    user_query = str(state.get("user_query") or "").lower()

    issue = str(facts.get("issue") or "").lower()
    response = str(facts.get("seller_response") or "").lower()

    text = user_query + " " + issue + " " + response

    # Detect whether the question is related to consumer disputes
    consumer_context = [
        "purchase", "purchased", "bought", "buy",
        "seller", "amazon", "flipkart", "shop",
        "order", "ordered", "refund", "return",
        "replacement", "warranty", "delivery",
        "delivered", "invoice", "consumer",
        "customer complaint", "grievance",
        "product", "service", "payment",
        "transaction", "repair", "e-commerce",
        "counterfeit", "fake", "defective",
        "damaged", "broken", "faulty",
        "misleading advertisement"
    ]

    has_consumer_context = any(
        word in text for word in consumer_context
    )

    # Reject clearly unrelated questions
    if not has_consumer_context:
        category = "OUT_OF_SCOPE"

    elif any(word in text for word in [
        "counterfeit", "fake", "duplicate", "spurious"
    ]):
        category = "COUNTERFEIT_PRODUCT"

    elif any(word in text for word in [
        "damaged", "damage", "defective",
        "broken", "cracked", "faulty",
        "physical damage", "not working"
    ]):
        category = "DEFECTIVE_PRODUCT"

    elif any(word in text for word in [
        "replacement refused", "replacement denied"
    ]):
        category = "REPLACEMENT_DENIED"

    elif any(word in text for word in [
        "no response", "ignored", "not responding"
    ]):
        category = "GRIEVANCE_IGNORED"

    elif any(word in text for word in [
        "refund refused", "refund denied",
        "refund rejected"
    ]):
        category = "REFUND_DENIED"

    else:
        # Could be another genuine consumer dispute
        category = "OTHER"

    return {
        "issue_category": category
    }
