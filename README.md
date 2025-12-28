# 🧠 AI Lead Qualifier (Deterministic LLM-Orchestrated System)

An AI-powered conversational lead qualification system that dynamically understands user intent, asks the right follow-up questions, and produces structured, high-quality leads — without hardcoding categories or flows.

Built to scale across lakhs of B2C and B2B categories, with suggestion bubbles, multilingual support, and production-grade control.

---

## 🔑 Core Design Philosophy

LLMs are probabilistic.  
Lead qualification is deterministic.  
So we wrapped probabilistic intelligence inside deterministic orchestration.

This system deliberately separates:
- What must be controlled → business rules, flow, stopping criteria
- What benefits from flexibility → language understanding and generation

The LLM is never allowed to decide:
- What to ask next
- When a lead is considered “ready”
- Which attributes are mandatory

All such decisions are enforced explicitly in code.

---

## 🚀 What This Project Does

- Extracts category automatically from free-text user input
- Dynamically generates a qualification schema per category
- Asks context-aware follow-up questions
- Displays suggestion bubbles to reduce seller typing effort
- Handles intent change mid-conversation
- Outputs structured lead data ready for downstream systems

---

## ✨ Key Features

- No hardcoded categories
- Dynamic question flow per category
- Few-shot prompting across all LLM tasks
- Hindi + English auto-detection
- Works for both B2C and B2B services
- Backend + frontend session reset
- Demo-ready frontend

---

## ❓ Why Not a Single Prompt or an Autonomous Agent?

A single prompt like “Ask the best follow-up question to qualify the lead” may work for demos, but fails in production.

This system avoids a fully autonomous agent because:
- Lead qualification requires deterministic outcomes
- Mandatory attributes must always be captured
- The flow must be auditable and debuggable
- Premature lead creation impacts revenue quality

Instead, the system uses multiple specialized prompts, each with a single responsibility:
- Category extraction
- Schema generation
- Question generation
- Attribute extraction

This provides control without sacrificing LLM intelligence.

---

## 🏗️ Architecture Overview

Frontend (HTML + JS)  
→ FastAPI (api.py)  
→ LeadQualifierSession  
→ Deterministic Orchestrator  
→ LLM (Groq + LLaMA 3 70B)

---

## 🧩 Architectural Principle

This system follows a planner–executor pattern:

Planner (Deterministic Code):
- Controls flow, state, business rules, and stopping conditions

Executor (LLM):
- Performs language understanding and generation within strict boundaries

This avoids the unpredictability of autonomous agents while remaining flexible and scalable.

---

## 📁 Project Structure

lead_qualifier/
- api.py
- app.py
- conversation/
  - orchestrator.py
  - session.py
  - state.py
  - language.py
  - category_extractor.py
  - question_generator.py
  - attribute_extractor.py
- schema/
  - schema_generator.py
- llm/
  - groq_client.py
  - prompts.py
- frontend/
  - index.html
  - style.css
  - app.js
- README.md
- .gitignore

---

## ⚙️ Tech Stack

Backend: Python, FastAPI, Uvicorn  
LLM: Groq API, LLaMA 3 70B  
Frontend: Vanilla HTML, CSS, JavaScript  
Prompting: Few-shot, structured JSON outputs

---

## 🛠️ Setup Instructions

1. (Optional) Create virtual environment  
   python3 -m venv .venv  
   source .venv/bin/activate

2. Install dependencies  
   pip3 install fastapi uvicorn pydantic

3. Set environment variable  
   export GROQ_API_KEY="your_groq_api_key"  
   Never commit API keys.

4. Run backend  
   uvicorn api:app --reload --port 8001  
   Verify at http://127.0.0.1:8001/docs

5. Run frontend (recommended)  
   cd frontend  
   python3 -m http.server 5500  
   Open http://127.0.0.1:5500/index.html

---

## 🧪 Example Conversations

B2C example:  
User: Looking for wedding photographer  
Bot: What type of photography do you need? [Wedding] [Pre-wedding] [Reception]

B2B example:  
User: Need industrial AC repair for factory  
Bot: What type of service do you need? What is the machine capacity? Which location?

---

## 🔄 Reset & Intent Switching

- Reset button clears frontend + backend session
- Changing intent mid-conversation automatically resets the flow

Example:  
User: looking for plumber  
User: actually need photographer  
→ Photographer flow starts cleanly

---

## 🧠 Lead Readiness Logic

A lead is marked ready only when:
- Mandatory attributes are filled
- Minimum qualification depth per category is met

This prevents premature or low-quality lead creation.

---

## 📋 Repository Requirements & Hygiene

Required:
- Python 3.9+
- FastAPI
- Uvicorn
- Groq API access

.gitignore must include:
- .venv/
- __pycache__/
- .env
- *.pyc
- .DS_Store

No-secrets policy:
- No API keys, tokens, credentials, or .env files in the repository
- All secrets injected via environment variables

---

## 🚧 Known Limitations (Demo Scope)

- Single-user in-memory session
- No authentication
- No persistent storage

These are intentionally scoped for demo clarity.

---

## 🔜 Possible Enhancements

- Multi-user sessions (Redis / DB)
- Lead quality scoring
- Near-me logic
- Analytics hooks
- WhatsApp / ChatGPT App integration

---

## 📌 Summary

This project demonstrates how LLMs can be used as controlled intelligence components, not autonomous decision-makers.

By embedding probabilistic language models inside deterministic orchestration, the system achieves predictability, scalability, debuggability, and production-aligned behavior.

This is not just a chatbot — it is a lead-qualification engine.
