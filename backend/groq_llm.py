
import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Safely check Streamlit Cloud Secrets
cloud_key = None

try:
    cloud_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    cloud_key = None

# Select the API key source
if cloud_key:
    api_key = cloud_key.strip()
    source = "Streamlit Secrets"
else:
    api_key = (os.getenv("GROQ_API_KEY") or "").strip()
    source = "Environment variable"

if not api_key:
    raise ValueError("GROQ_API_KEY is missing")

# Diagnostic information (never print the actual key)
print("Groq key source:", source)
print("Groq key prefix:", api_key[:4])
print("Groq key length:", len(api_key))
print(
    "Groq key fingerprint:",
    hashlib.sha256(api_key.encode()).hexdigest()[:12]
)

groq_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0.1,
    max_tokens=2000,
    timeout=60,
    max_retries=1
)

