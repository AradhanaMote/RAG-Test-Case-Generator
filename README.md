# RAG-Based Test Case Generator

![App UI Screenshot](assets/ui_screenshot.png)
<sub><sup>Figure: Streamlit front-end to upload documents and generate test cases</sup></sub>

## Overview
This project implements an autonomous QA agent designed to streamline test case creation and accelerate end-to-end web app verification. Built on Retrieval-Augmented Generation (RAG) principles, it builds a knowledge base from your requirements and generates documentation-grounded test cases. With one click, selected cases can be converted to runnable Selenium (Python) scripts.

### Key Features
- **Document Upload:** Supports txt, md, and pdf support documentation, plus UI HTML.
- **AI Test Case Generation:** Produces actionable, context-grounded test cases from your documentation.
- **Selenium Script Export:** Generate Python Selenium scripts for chosen test cases.
- **Modern UI:** User-friendly web application built with Streamlit.
- **Flexible RAG Backend:** Swap out LLMs or vector DBs with minimal code changes.

---

## Project Structure
```plaintext
qa_agent_assignment/
├── api.py                 # FastAPI backend serving the app's core APIs
├── ui.py                  # Streamlit-based frontend
├── parser_utils.py        # Document parsing and chunking logic
├── vectorstore.py         # Vector database (Chroma) wrapper
├── rag_agent.py           # RAG orchestration and LLM API integration
├── templates/
│   └── checkout.html      # Sample HTML used as target for test generation
├── support_docs/          # Sample requirement and guide docs
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Windows 11 recommended (tested; 11th gen Dell i5+ is sufficient)
- Python 3.10 or 3.11
- Chrome browser and ChromeDriver (ensure versions match)

### Setup

1. **Clone the repo:**
    ```powershell
    git clone https://github.com/AradhanaMote/RAG-Test-Case-Generator.git
    cd RAG-Test-Case-Generator
    ```

2. **Set up a Python virtual environment:**
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Prepare sample files:**  
   Move `checkout.html` into `templates/` and sample docs into `support_docs/`.

4. **Configure your LLM provider:**  
   For OpenAI (example):
    ```powershell
    setx OPENAI_API_KEY "sk-..."
    ```  

### Running the App

1. **Start the backend API:**
    ```powershell
    uvicorn api:app --reload --port 8000
    ```
2. **Start the Streamlit UI:**
    ```powershell
    streamlit run ui.py
    ```

3. **In the UI:**
    - Upload your requirements/support documentation and the target HTML.
    - Click “Build Knowledge Base.”
    - Enter a prompt for test case generation.
    - Select cases and generate Selenium scripts as needed.

---

## Customization Notes

- **LLM Flexibility:**  
  Swap out OpenAI for local LLMs, Hugging Face models, or Ollama via `rag_agent.py`.

- **Vector Store:**  
  Uses Chroma by default. Swap to FAISS or Qdrant by editing `vectorstore.py`.

---

## Screenshot

![RAG-Based Test Case Generator UI](assets/ui_screenshot.png)

*The UI makes it simple to upload documents, generate test cases, and export Selenium scripts.*

---

## License
MIT

---

*Project maintained by [AradhanaMote](https://github.com/AradhanaMote).*
