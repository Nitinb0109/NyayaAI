
import re
from pydantic import BaseModel, Field
from typing import Optional


class IntakeDetails(BaseModel):
    product: Optional[str] = None
    purchase_amount: Optional[float] = None
    purchase_date: Optional[str] = None

    issue: Optional[str] = None
    seller_response: Optional[str] = None
    platform: Optional[str] = None

    evidence: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)


def extract_amount(text):
    match = re.search(
        r"(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d{1,2})?)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1).replace(",", ""))

    return None


def extract_date(text):
    patterns = [
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def extract_platform(text):
    platforms = [
        "Amazon",
        "Flipkart",
        "Meesho",
        "Myntra",
        "Ajio",
        "Snapdeal"
    ]

    for platform in platforms:
        if re.search(rf"\b{platform}\b", text, re.IGNORECASE):
            return platform

    return None


def extract_product(text):
    patterns = [
        r"(?:purchased|bought|ordered)\s+(?:a|an|the)?\s*(.{2,80}?)\s+for\s+(?:₹|rs\.?|inr)",
        r"(?:product|item)\s*:\s*(.{2,80}?)(?:[.,\n]|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_issue(text):
    issue_keywords = [
        "cracked screen",
        "physical damage",
        "damaged",
        "defective",
        "counterfeit",
        "fake product",
        "refund",
        "replacement",
        "wrong product",
        "not delivered",
        "missing item"
    ]

    found = [
        keyword for keyword in issue_keywords
        if keyword in text.lower()
    ]

    return ", ".join(found) if found else None


def extract_seller_response(text):
    patterns = [
        r"seller.{0,100}(?:refused|rejected|denied|agreed|accepted).{0,100}",
        r"(?:refused|rejected|denied).{0,100}(?:refund|replacement).{0,100}"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def extract_evidence(text):
    evidence_keywords = {
        "invoice": "Purchase invoice",
        "photograph": "Product photographs",
        "photo": "Product photographs",
        "screenshot": "Conversation screenshots",
        "order details": "Order details",
        "video": "Product unboxing/video evidence",
        "payment receipt": "Payment receipt"
    }

    found = []

    for keyword, label in evidence_keywords.items():
        if keyword in text.lower() and label not in found:
            found.append(label)

    return found


def intake_agent(state):

    user_query = state["user_query"]

    extracted_facts = IntakeDetails(
        product=extract_product(user_query),
        purchase_amount=extract_amount(user_query),
        purchase_date=extract_date(user_query),
        issue=extract_issue(user_query),
        seller_response=extract_seller_response(user_query),
        platform=extract_platform(user_query),
        evidence=extract_evidence(user_query)
    )

    missing = []

    required_fields = {
        "product": "Product name",
        "purchase_amount": "Purchase amount",
        "purchase_date": "Purchase date",
        "issue": "Description of the problem",
        "platform": "Marketplace/platform name"
    }

    for field, label in required_fields.items():
        if getattr(extracted_facts, field) is None:
            missing.append(label)

    extracted_facts.missing_information = missing

    facts = extracted_facts.model_dump()

    return {
        "extracted_facts": facts,
        "missing_information": missing
    }
