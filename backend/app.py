import os
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.pipeline import RAGPipeline
import uvicorn
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # <-- Make sure .env file is read

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", None)

print("OpenAI Key Loaded:", OPENAI_KEY is not None)  # Debug: ensure key is loaded

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
# Request model for /ask endpoint
# -----------------------------
class QuestionRequest(BaseModel):
    query: str
    top_k: int = 5

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
async def ask(req: QuestionRequest):
    """
    Ask a question and get answer from the RAG pipeline
    """
    try:
        res = pipeline.answer(req.query, top_k=req.top_k)
        return res
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}", exc_info=True)
        return {"error": "Internal Server Error", "details": str(e)}


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
# Startup event logs
# -----------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("Starting backend...")
    logger.info(f"Chunks indexed at startup: {pipeline.indexer.count()}")

# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
