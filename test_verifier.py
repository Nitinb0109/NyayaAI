
from agents.verifier import verifier_agent

state = {
    "legal_answer": """
    Under Rule 6(3), a seller cannot refuse
    a refund for defective goods.

    Section 999 of the Consumer Protection Act
    provides an additional remedy.
    """,

    "retrieved_context": [
        {
            "content": """
            Rule 6(3): No seller shall refuse
            to refund consideration if goods
            are defective or deficient.
            """
        }
    ]
}

result = verifier_agent(state)

print(result)
