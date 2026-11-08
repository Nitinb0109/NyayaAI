from backend.groq_llm import groq_llm


def document_generator_agent(state):

    facts = state["extracted_facts"]
    category = state["issue_category"]
    verification = state.get("verification_result", {})

    # Do not rely on unsupported legal claims
    if verification.get("status") == "REVIEW_REQUIRED":
        warning = (
            "Some legal references were not verified. "
            "Do not include unsupported legal claims."
        )
    else:
        warning = "Use only legal claims supported by retrieved context."

    prompt = f"""
    You are the Document Generator Agent of NyayaAI.

    Draft a preliminary consumer complaint based on
    the following information.

    CONSUMER FACTS:
    {facts}

    DISPUTE CATEGORY:
    {category}

    VERIFICATION REPORT:
    {verification}

    INSTRUCTIONS:
    1. Draft in simple, professional English.
    2. Never invent names, dates, amounts or order IDs.
    3. Use placeholders for missing information.
    4. Do not invent legal sections or provisions.
    5. Do not claim that the consumer will definitely win.
    6. Clearly distinguish allegations from established facts.
    7. Include the consumer's requested remedy.
    8. {warning}

    DOCUMENT FORMAT:

    CONSUMER COMPLAINT

    1. Consumer Details
    2. Seller and Platform Details
    3. Purchase Details
    4. Description of the Problem
    5. Steps Already Taken
    6. Evidence Available
    7. Relief Requested
    8. Declaration

    Mark missing information with [TO BE PROVIDED].

    Add a note that this is a preliminary AI-generated
    draft and should be reviewed before submission.
    """

    response = groq_llm.invoke(prompt)

    return {
        "generated_document": response.content
    }