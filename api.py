from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
from vectorstore import VectorStore
from parser_utils import parse_file_to_text

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) 

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize a vector store (Chroma)
vector_store = VectorStore(str(BASE_DIR / "chroma_db"))

@app.post('/upload-support')
async def upload_support(file: UploadFile = File(...)):
    dest = UPLOAD_DIR / file.filename
    with open(dest, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    text = parse_file_to_text(str(dest))
    return {"status": "ok", "filename": file.filename, "text_preview": text[:500]}

@app.post('/build-knowledgebase')
async def build_knowledgebase(files: list[UploadFile] = File(...)):
    # Parse, chunk, embed and ingest
    docs = []
    for file in files:
        dest = UPLOAD_DIR / file.filename
        with open(dest, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        text = parse_file_to_text(str(dest))
        docs.append({"text": text, "meta": {"source": file.filename}})
    vector_store.ingest_documents(docs)
    return {"status": "knowledge_base_built", "documents_ingested": len(docs)}

@app.post('/query')
async def query_agent(query: str = Form(...), top_k: int = Form(5)):
    # retrieve relevant context and return it
    results = vector_store.search(query, top_k=top_k)
    return {"query": query, "results": results}

@app.post('/generate-script')
async def generate_script(test_case_json: dict = Form(...)):
    # This endpoint is intentionally left light — actual script generation occurs on the client by calling the RAG agent wrapper.
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
