from sentence_transformers import SentenceTransformer
import chromadb
from typing import List


class VectorStore:
    def __init__(self, persist_directory: str = './chromadb'):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name='qa_kb')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        chunks = []
        i = 0
        while i < len(text):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
            i += chunk_size - overlap
        return chunks
    
    def ingest_documents(self, docs: List[dict]):
        for d in docs:
            text = d.get('text', '')
            source = d.get('meta', {}).get('source', 'unknown')
            chunks = self._chunk_text(text)
            
            if not chunks:
                continue
            
            embeddings = self.embedder.encode(chunks, show_progress_bar=False)
            ids = [f"{source}__{i}" for i in range(len(chunks))]
            metadatas = [{"source": source}] * len(chunks)
            
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings.tolist()
            )
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        q_emb = self.embedder.encode([query])[0]
        res = self.collection.query(
            query_embeddings=[q_emb.tolist()],
            n_results=top_k
        )
        
        out = []
        if res.get('documents') and len(res['documents']) > 0:
            docs = res['documents'][0]
            metas = res.get('metadatas', [[]])[0]
            distances = res.get('distances', [[]])[0]
            
            for doc, meta, dist in zip(docs, metas, distances):
                out.append({
                    'document': doc,
                    'meta': meta,
                    'distance': dist
                })
        
        return out