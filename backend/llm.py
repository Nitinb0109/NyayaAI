
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables from .env (local development)
load_dotenv()


# Get API key from Streamlit Cloud secrets first
try:
    api_key = st.secrets.get("GOOGLE_API_KEY")
except Exception:
    api_key = None


# Fallback to local .env file
api_key = api_key or os.getenv("GOOGLE_API_KEY")


if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")


# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
    temperature=0.2
)


# Generate legal answer using retrieved context
def generate_legal_answer(question, context):

    prompt = f"""
    You are NyayaAI, an AI assistant specializing in
    Indian consumer protection law.

    Answer the user's question using ONLY the legal
    context provided below.

    STRICT RULES:

    1. Use only provisions present in the retrieved context.
    2. Never invent sections, rules, judgments or deadlines.
    3. Cite the exact legal source, including:
       - Act or Rule name
       - Section or Rule number
       - Sub-section, sub-rule, or clause number, if available
       - PDF page number as a source reference
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

    LEGAL CONTEXT:
    {context}

    USER QUESTION:
    {question}

    Provide your answer in this structure:

    1. Understanding the problem
    2. Relevant legal provisions
    3. Possible actions
    4. Evidence required
    5. Important limitations
    6. Important disclaimer

    Remember: You are an AI assistant, not a qualified lawyer.
    """

    response = llm.invoke(prompt)

    return extract_response_text(response)


# Convert Gemini response into plain text
def extract_response_text(response):

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )

    return str(content)
