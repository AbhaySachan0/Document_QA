# core/document_loader.py
import io
import pdfplumber
from bs4 import BeautifulSoup
import markdown
from typing import Tuple

def load_pdf_from_bytes(data: bytes) -> str:
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n\n".join(pages)

def load_html_from_text(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator="\n")

def load_markdown_from_text(md_text: str) -> str:
    html = markdown.markdown(md_text)
    return load_html_from_text(html)

def load_document(filename: str, content_bytes: bytes) -> Tuple[str, str]:
    """
    Returns tuple (mime_hint, text)
    mime_hint is one of: "pdf", "md", "html", "txt"
    """
    fn = filename.lower()
    if fn.endswith(".pdf"):
        text = load_pdf_from_bytes(content_bytes)
        return "pdf", text
    if fn.endswith(".md") or fn.endswith(".markdown"):
        text = load_markdown_from_text(content_bytes.decode("utf-8", errors="ignore"))
        return "md", text
    if fn.endswith(".html") or fn.endswith(".htm"):
        text = load_html_from_text(content_bytes.decode("utf-8", errors="ignore"))
        return "html", text
    # fallback: try decode as text
    try:
        text = content_bytes.decode("utf-8")
        return "txt", text
    except Exception:
        # last resort: return empty
        return "unknown", ""
