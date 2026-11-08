import time
from backend.groq_llm import groq_llm

print("Testing Groq connection...")

try:
    start = time.perf_counter()

    response = groq_llm.invoke(
        "Explain the Consumer Protection Act, 2019 in India "
        "in exactly three simple sentences."
    )

    end = time.perf_counter()

    print("\nGroq Response:")
    print(response.content)

    print("\nResponse time:", round(end - start, 2), "seconds")

except Exception as e:
    print("Groq Error:", str(e))