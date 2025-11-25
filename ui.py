import streamlit as st
import requests
import json
from pathlib import Path
from parser_utils import parse_file_to_text
from rag_agent import build_test_case_prompt, generate_with_llm, build_script_prompt
from vectorstore import VectorStore

BASE = Path(__file__).parent
UPLOAD_DIR = BASE / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="RAG Test Case Generator",
    page_icon="🤖",
    layout="wide"
)

if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()

if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []

if 'context_chunks' not in st.session_state:
    st.session_state.context_chunks = []

st.title("🤖 RAG-Based Test Case Generator")

st.sidebar.header("📁 Document Upload")
uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    type=['txt', 'md', 'json', 'pdf', 'html', 'htm'],
    accept_multiple_files=True
)

if uploaded_files:
    if st.sidebar.button("Ingest Documents"):
        with st.spinner("Processing documents..."):
            docs = []
            for file in uploaded_files:
                save_path = UPLOAD_DIR / file.name
                with open(save_path, 'wb') as f:
                    f.write(file.getbuffer())
                
                text = parse_file_to_text(str(save_path))
                docs.append({
                    'text': text,
                    'meta': {'source': file.name}
                })
            
            st.session_state.vector_store.ingest_documents(docs)
            st.sidebar.success(f"Ingested {len(docs)} documents!")

st.header("Generate Test Cases")
user_query = st.text_area(
    "Enter your test case requirements:",
    placeholder="e.g., Generate test cases for login functionality with valid and invalid credentials"
)

col1, col2 = st.columns([1, 1])

with col1:
    top_k = st.slider("Number of context chunks", 1, 10, 5)

with col2:
    max_tokens = st.slider("Max tokens for generation", 256, 2048, 1024)

if st.button("Generate Test Cases", type="primary"):
    if not user_query:
        st.warning("Please enter a query")
    else:
        with st.spinner("Searching knowledge base..."):
            results = st.session_state.vector_store.search(user_query, top_k=top_k)
            st.session_state.context_chunks = [r['document'] for r in results]
            
        with st.spinner("Generating test cases..."):
            prompt = build_test_case_prompt(st.session_state.context_chunks, user_query)
            response = generate_with_llm("You are a QA test case generator.", prompt, max_tokens)
            
            st.subheader("LLM Output")
            st.text_area("Raw Response:", response, height=300)
            
            try:
                response_clean = response.strip()
                if response_clean.startswith('```json'):
                    response_clean = response_clean[7:]
                if response_clean.startswith('```'):
                    response_clean = response_clean[3:]
                if response_clean.endswith('```'):
                    response_clean = response_clean[:-3]
                response_clean = response_clean.strip()
                
                test_cases = json.loads(response_clean)
                st.session_state.test_cases = test_cases if isinstance(test_cases, list) else [test_cases]
                st.success(f"✅ Generated {len(st.session_state.test_cases)} test case(s)!")
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse test cases as JSON: {e}")

if st.session_state.test_cases:
    st.header("📋 Generated Test Cases")
    
    for idx, tc in enumerate(st.session_state.test_cases):
        with st.expander(f"**Test Case {idx + 1}: {tc.get('Test_Scenario', 'N/A')}**", expanded=False):
            st.json(tc)
            
            st.subheader("Generate Selenium Script")
            
            html_input = st.text_input(
                "Enter target page URL or local HTML file path:",
                key=f"html_input_{idx}",
                placeholder="https://example.com/checkout or path/to/file.html"
            )
            
            if st.button(f"🔧 Generate Selenium Script", key=f"gen_script_{idx}"):
                if not html_input:
                    st.warning("Please enter a URL or file path")
                else:
                    try:
                        with st.spinner("Fetching HTML content..."):
                            if html_input.startswith('http'):
                                html_content = requests.get(html_input, timeout=10).text
                            else:
                                html_content = Path(html_input).read_text(encoding='utf-8')
                        
                        with st.spinner("Generating Selenium script..."):
                            script_prompt = build_script_prompt(html_content, tc, st.session_state.context_chunks)
                            script = generate_with_llm("You are a Selenium automation expert.", script_prompt, 2048)
                            
                            script_clean = script.strip()
                            if script_clean.startswith('```python'):
                                script_clean = script_clean[9:]
                            if script_clean.startswith('```'):
                                script_clean = script_clean[3:]
                            if script_clean.endswith('```'):
                                script_clean = script_clean[:-3]
                            script_clean = script_clean.strip()
                            
                            st.code(script_clean, language='python')
                            
                            st.download_button(
                                "⬇️ Download Script",
                                script_clean,
                                file_name=f"test_case_{idx + 1}.py",
                                mime="text/x-python",
                                key=f"download_{idx}"
                            )
                            
                            st.success("✅ Script generated successfully!")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error fetching URL: {e}")
                    except FileNotFoundError:
                        st.error(f"File not found: {html_input}")
                    except Exception as e:
                        st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("📌 Upload documents → Generate test cases → Generate Selenium scripts")