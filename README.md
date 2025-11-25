# Autonomous QA Agent (Test Case + Selenium Script Generation)

## Overview
This project implements an autonomous QA agent that builds a knowledge base from support documents and an HTML target (checkout.html), generates documentation-grounded test cases, and converts selected test cases into runnable Selenium (Python) scripts.

## Project structure
```
qa_agent_assignment/
├── api.py                 # FastAPI backend
├── ui.py                  # Streamlit frontend
├── parser_utils.py        # Document parsing and chunking
├── vectorstore.py         # Chroma vector DB wrapper
├── rag_agent.py           # RAG orchestration and LLM interface
├── templates/
│   └── checkout.html      # The target single-page app (provided)
├── support_docs/          # Example support docs (product_specs.md, ui_ux_guide.txt, api_endpoints.json)
├── requirements.txt
└── README.md
```

## Prerequisites
- Windows 11 machine (tested) — 11th gen Dell i5 is fine
- Python 3.10 or 3.11
- Chrome browser + matching ChromeDriver version

## Setup (PowerShell / CMD)
1. Clone or copy the project to a folder: `C:\path\to\AutonomousQAAgent`
2. Create virtual env and activate:
   ```powershell
   cd C:\path\to\AutonomousQAAgent
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Put the provided `checkout.html` into `templates/checkout.html` and example support docs into `support_docs/`.
4. Set environment variables for the LLM provider you want to use (example: OpenAI):
   ```powershell
   setx OPENAI_API_KEY "sk-..."
   ```

## Run
1. Start backend: `uvicorn api:app --reload --port 8000`
2. Start UI: `streamlit run ui.py`
3. In the Streamlit UI: Upload support documents and checkout.html (or use provided files), then click "Build Knowledge Base". Ask the agent to generate test cases and generate Selenium scripts for selected test cases.

## Notes
- LLM calls are abstracted in `rag_agent.py`. You can replace the `generate_with_llm` function implementation with your preferred provider (OpenAI, local HF model, Ollama, etc.).
- Vector DB uses Chroma by default. If you'd like FAISS or Qdrant, change `vectorstore.py` accordingly.

## Provided assignment PDF
The original assignment PDF included with the project is available at: `/mnt/data/Assignment - 1.pdf`
