# core/chunker.py
from typing import List
import re

def simple_sentence_split(text: str) -> List[str]:
    # preserves lines and breaks sensibly
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    return paragraphs

def chunk_text(
    text: str,
    max_chunk_chars: int = 2000,
    overlap_chars: int = 200
) -> List[str]:
    """
    Token-aware chunking would be ideal, but to keep dependency light we chunk by characters.
    Default: ~2000 characters per chunk with overlap.
    Returns list of chunk strings.
    """
    if not text:
        return []
    paragraphs = simple_sentence_split(text)
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 1 <= max_chunk_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current.strip())
            # if paragraph itself very long, slice it
            if len(p) > max_chunk_chars:
                start = 0
                while start < len(p):
                    end = min(len(p), start + max_chunk_chars)
                    chunks.append(p[start:end])
                    start = end - overlap_chars if end != len(p) else end
                current = ""
            else:
                current = p
    if current:
        chunks.append(current.strip())
    # add small overlaps by merging neighbor tails/heads (optional)
    return chunks
