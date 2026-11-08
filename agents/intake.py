import json
from urllib import response
from pydantic import BaseModel, Field
from typing import Optional

from sympy import content
from backend.llm import llm


class IntakeDetails(BaseModel):

    product: Optional[str] = None
    purchase_amount: Optional[float] = None
    purchase_date: Optional[str] = None

    issue: Optional[str] = None
    seller_response: Optional[str] = None
    platform: Optional[str] = None

    evidence: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)


def intake_agent(state):

    user_query = state["user_query"]

    prompt = f"""
    You are the Intake Agent of NyayaAI,
    an Indian consumer dispute assistant.

    Extract the following information:
    - product
    - purchase_amount
    - purchase_date
    - issue
    - seller_response
    - platform
    - evidence
    - missing_information

    Rules:
    1. Never invent information.
    2. Use null for unavailable values.
    3. Use a number for purchase_amount.
    4. Use arrays for evidence and missing_information.
    5. Return ONLY valid JSON. No markdown or explanation.

    Expected JSON structure:
    {{
        "product": null,
        "purchase_amount": null,
        "purchase_date": null,
        "issue": null,
        "seller_response": null,
        "platform": null,
        "evidence": [],
        "missing_information": []
    }}

    USER COMPLAINT:
    {user_query}
    """

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        raw_output = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    else:
        raw_output = content.strip()
    # Remove markdown code fences if Gemini returns them
    if raw_output.startswith("```"):
        raw_output = raw_output.replace("```json", "", 1)
        raw_output = raw_output.replace("```", "").strip()

    # Parse and validate JSON
    result = IntakeDetails.model_validate_json(raw_output)

    extracted_facts = result.model_dump()

    return {
        "extracted_facts": extracted_facts,
        "missing_information": extracted_facts["missing_information"]
    }