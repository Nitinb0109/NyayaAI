
import re


def normalize_text(value):
    if isinstance(value, str):
        return value

    if isinstance(value, list):
        return "\n".join(
            item.get("text", "")
            for item in value
            if isinstance(item, dict)
        )

    return str(value)


def verifier_agent(state):

    answer = normalize_text(
        state.get("legal_answer", "")
    )

    documents = state.get("retrieved_context", [])

    context = "\n".join(
        normalize_text(doc.get("content", ""))
        for doc in documents
    )

    # Extract Act section references
    cited_sections = set(
        re.findall(
            r"\bSections?\s+(\d+)",
            answer,
            flags=re.IGNORECASE
        )
    )

    supported_sections = set(
        re.findall(
            r"\bSections?\s+(\d+)",
            context,
            flags=re.IGNORECASE
        )
    )

    # Extract E-Commerce Rule references
    cited_rules = set(
        re.findall(
            r"\bRule\s+(\d+)",
            answer,
            flags=re.IGNORECASE
        )
    )

    supported_rules = set(
        re.findall(
            r"\bRule\s+(\d+)",
            context,
            flags=re.IGNORECASE
        )
    )

    unsupported_sections = sorted(
        cited_sections - supported_sections
    )

    unsupported_rules = sorted(
        cited_rules - supported_rules
    )

    report = {
        "cited_sections": sorted(cited_sections),
        "unsupported_sections": unsupported_sections,
        "cited_rules": sorted(cited_rules),
        "unsupported_rules": unsupported_rules,
        "status": (
            "REVIEW_REQUIRED"
            if unsupported_sections or unsupported_rules
            else "BASIC_CHECK_PASSED"
        )
    }

    return {
        "verification_result": report
    }

