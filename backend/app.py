# backend/app.py
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from core.pipeline import RAGPipeline
import uvicorn
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # <-- Make sure .env file is read

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", None)

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI()

# Allow frontend (React/Vite default ports)
origins = [
    "http://localhost:3000",  # React (CRA)
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pipeline (in-memory index)
# -----------------------------
pipeline = RAGPipeline(
    embedding_model_name=EMBED_MODEL,
    openai_api_key=OPENAI_KEY
)

# -----------------------------
# Routes
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    Upload and ingest a file into the RAG pipeline
    """
    content = await file.read()
    count = pipeline.ingest_bytes(file.filename, content)
    return {
        "message": f"Ingested {count} chunks from {file.filename}",
        "chunks": count
    }


@app.post("/ask")
async def ask(question: str = Form(...), top_k: int = Form(5)):
    """
    Ask a question and get answer from the RAG pipeline
    """
    res = pipeline.answer(question, top_k=top_k)
    return res


@app.get("/")
async def root():
    """
    Health check
    """
    return {"status": "ok", "service": "backend running"}


@app.get("/info")
def info():
    """
    Returns number of chunks currently indexed
    """
    return {"chunks_indexed": pipeline.indexer.count()}


# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
