from typing import List
import re

def simple_sentence_split(text: str) -> List[str]:
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    return paragraphs

def chunk_text(
    text: str,
    max_chunk_chars: int = 2000,
    overlap_chars: int = 200
) -> List[str]:
    if not text:
        return []
    paragraphs = simple_sentence_split(text)
    chunks = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chunk_chars:  # +2 for "\n\n"
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current.strip())
                # Add overlap by taking last overlap_chars characters
                overlap_text = current[-overlap_chars:] if len(current) > overlap_chars else current
                current = overlap_text
            # If paragraph itself very long, slice it
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

    return chunks
