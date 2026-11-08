from typing import TypedDict


class NyayaState(TypedDict, total=False):

    # Original user input
    user_query: str

    # Information extracted by Intake Agent
    extracted_facts: dict

    # Consumer dispute category
    issue_category: str

    # Missing information
    missing_information: list

    # Retrieved legal documents
    retrieved_context: list

    # Legal explanation
    legal_answer: str

    # Generated legal document
    generated_document: str

    # Verification results
    verification_result: str

    # Final response
    final_response: str