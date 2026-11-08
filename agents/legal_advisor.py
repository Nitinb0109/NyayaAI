
from backend.llm import llm


def legal_advisor_agent(state):

    facts = state["extracted_facts"]
    category = state["issue_category"]
    documents = state["retrieved_context"]

    # Prepare legal context with source and page information
    context = ""

    for doc in documents:
        context += f"""
Source: {doc['source']}
Page: {doc['page']}
Legal Text:
{doc['content']}
--------------------------------
"""

    prompt = f"""
You are NyayaAI, an AI assistant explaining
Indian consumer protection law.

Your task is to explain the consumer's legal
options using ONLY the retrieved legal context.

CONSUMER FACTS:
{facts}

ISSUE CATEGORY:
{category}

RETRIEVED LEGAL CONTEXT:
{context}

STRICT RULES:
1. Use only provisions present in the retrieved context.
2. Never invent sections, rules, judgments or deadlines.
3. Cite the exact Act/Rule and page number when visible.
4. If the retrieved text is incomplete, mention this limitation.
5. Do not guarantee any legal outcome.
6. Distinguish legal provisions from practical suggestions.
7. Explain everything in simple English.
8. If the available context is insufficient, say so.
9. Never cite a PDF page number as if it were a legal provision.
10. Always identify the actual Rule, sub-rule, clause,
    or Section before mentioning the PDF page number.
11. Use this citation format:
    Rule 5(1)(b), Consumer Protection (E-Commerce)
    Rules, 2020 (PDF page 5).
12. If the exact Rule or clause cannot be identified
    from the retrieved text, write:
    "Relevant provision identified on PDF page X;
    exact clause requires verification."
13. Never infer legal obligations from incomplete OCR text.
14. Do not assume that a provision applies to every
    e-commerce business model. Check its applicability
    and conditions in the retrieved context.
FORMAT YOUR ANSWER:

1. Understanding the Problem
Summarize the consumer's situation.

2. Relevant Legal Provisions
Explain the relevant sections or rules with citations.

3. Possible Actions
Give practical steps the consumer can consider.

4. Evidence Required
List useful evidence based on the facts.

5. Missing Information
Mention information needed for a more complete assessment.

6. Important Disclaimer
Explain that NyayaAI provides general legal information,
not professional legal representation.
"""

    response = llm.invoke(prompt)

    # Convert Gemini response into plain text
    content = response.content

    if isinstance(content, list):
        answer = "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )
    else:
        answer = str(content)

    return {
        "legal_answer": answer
    }
