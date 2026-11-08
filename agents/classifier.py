def classifier_agent(state):

    facts = state["extracted_facts"]

    issue = str(facts.get("issue") or "").lower()
    response = str(facts.get("seller_response") or "").lower()

    text = issue + " " + response

    if any(word in text for word in [
        "counterfeit", "fake", "duplicate", "spurious"
    ]):
        category = "COUNTERFEIT_PRODUCT"

    elif any(word in text for word in [
        "damaged",
    "damage",
    "defective",
    "broken",
    "cracked",
    "faulty",
    "physical damage",
    "not working"
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
        category = "OTHER"

    return {
        "issue_category": category
    }