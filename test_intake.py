from agents.intake import intake_agent

state = {
    "user_query": """
    I purchased a Samsung mobile phone for Rs. 20,000
    from Amazon on 10 October 2026.

    The phone arrived with a damaged screen.
    I contacted the seller, but they refused to
    provide a refund.

    I have the invoice and photographs of the damage.
    """
}

result = intake_agent(state)

print("\n========== INTAKE AGENT OUTPUT ==========\n")

print("Extracted Facts:")

for key, value in result["extracted_facts"].items():
    print(f"{key}: {value}")

print("\nMissing Information:")
print(result["missing_information"])