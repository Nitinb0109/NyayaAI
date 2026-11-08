

import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Prioritize Streamlit Cloud Secrets
try:
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    api_key = None

# Fallback for local development
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing")

api_key = api_key.strip()

# Safe diagnostic information
print("Groq key source:",
      "Streamlit Secrets" if st.secrets.get("GROQ_API_KEY") else "Environment variable")
print("Groq key prefix:", api_key[:4])
print("Groq key length:", len(api_key))
print("Groq key fingerprint:",
      hashlib.sha256(api_key.encode()).hexdigest()[:12])

groq_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0.1,
    max_tokens=2000,
    timeout=60,
    max_retries=1
)
