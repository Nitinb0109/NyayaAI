# NyayaAI – AI-Powered Indian Consumer Legal Assistant

## Problem Statement

Many consumers in India face problems such as defective products, refund rejections, counterfeit products, replacement denials, and unresolved e-commerce complaints.

However, consumers often struggle to understand their legal rights, identify relevant consumer-protection laws, and prepare a formal complaint. Finding the correct legal provisions and understanding how to take action can be difficult for someone without a legal background.

## Our Solution

NyayaAI is an AI-powered Indian Consumer Legal Assistant that helps users understand consumer disputes and take informed next steps.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant provisions from Indian consumer-protection laws and generate contextual legal explanations.

Users can:
- Describe their consumer-related problem in natural language.
- Identify the category of their consumer dispute.
- Understand relevant legal provisions in simple language.
- Get possible actions and guidance for their situation.
- Generate a structured preliminary consumer complaint draft.

## What I Added / Key Implementations

### 1. Multi-Agent Architecture Using LangGraph
Implemented a multi-agent workflow where different agents handle specific responsibilities, including intake, classification, legal research, legal advice, verification, and complaint generation.

### 2. Out-of-Scope Query Detection
Added a scope-checking mechanism to identify queries unrelated to consumer disputes. Such queries are routed to a separate Out-of-Scope Agent instead of proceeding through the legal research workflow.

### 3. BM25-Based Legal Retrieval
Implemented BM25 retrieval to find relevant legal provisions from the Consumer Protection Act, 2019, and Consumer Protection (E-Commerce) Rules, 2020.

### 4. Context-Aware Legal Assistance
Connected the retrieved legal context with the LLM so that legal explanations are generated based on relevant provisions rather than relying only on general model knowledge.

### 5. Preliminary Complaint Generation
Added a document-generation agent that creates structured consumer complaint drafts based on the user's dispute details.

### 6. Verification Stage
Added a verifier agent to review the generated legal response as part of the workflow.

## Technology Stack

- Python
- Streamlit
- LangGraph
- Groq API – GPT-OSS-120B
- BM25 Retrieval
- Retrieval-Augmented Generation (RAG)

## Legal Knowledge Base

- Consumer Protection Act, 2019
- Consumer Protection (E-Commerce) Rules, 2020

## Disclaimer

NyayaAI is an experimental AI-based legal assistance project for general informational purposes. It does not replace professional legal advice. Generated explanations and complaint drafts should be independently reviewed before formal use.
