# backend/app.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from core.pipeline import RAGPipeline
import uvicorn

# read env
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", None)

app = FastAPI()
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# single pipeline instance (in-memory index)
pipeline = RAGPipeline(embedding_model_name=EMBED_MODEL, openai_api_key=OPENAI_KEY)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    count = pipeline.ingest_bytes(file.filename, content)
    return {"message": f"ingested {count} chunks from {file.filename}", "chunks": count}

@app.post("/ask")
async def ask(question: str = Form(...), top_k: int = Form(5)):
    res = pipeline.answer(question, top_k=top_k)
    return res

@app.get("/info")
def info():
    return {"chunks_indexed": pipeline.indexer.count()}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
