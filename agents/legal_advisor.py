
from backend.groq_llm import groq_llm


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
10. For marketplace purchases, prioritize Rule 6(3)
    when the retrieved text supports a defective-product
    refund or return issue.

11. Do not use Rule 8(4) as a substitute for Rule 6(3).
    Clearly distinguish marketplace and inventory
    e-commerce entities.

12. If the user says the product arrived damaged,
    do not assume the damage was caused by the consumer.

13. Preserve all user-provided facts accurately.
    Never change the product, amount, dates, platform,
    or sequence of events.

14. Classify the dispute using the extracted facts.
    A damaged or cracked product should be identified
    as a defective-product dispute, not OTHER.

15. Do not state that a provision guarantees a refund.
    Explain that the consumer may seek the relevant remedy.
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

    response = groq_llm.invoke(prompt)

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
