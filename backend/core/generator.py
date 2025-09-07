import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Change as needed

class Generator:
    def __init__(self, api_key: str = None, model: str = OPENAI_MODEL):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required: set OPENAI_API_KEY env var or pass api_key")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def build_prompt(self, question: str, contexts: List[Dict]) -> str:
        """
        Build a prompt using contexts and question.
        """
        ctx_blocks = []
        for c in contexts:
            header = f"[Source: {c.get('source','unknown')} | chunk:{c.get('chunk_id','?')} | score:{c.get('score', 0):.3f}]"
            ctx_blocks.append(header + "\n" + c.get("text", ""))
        ctx = "\n\n---\n\n".join(ctx_blocks)

        prompt = (
            "You are a helpful assistant. Use ONLY the context below to answer the question. "
            "If the answer cannot be found in the context, say 'I don't know'. Be concise and include short citations like [Source: filename, chunk_id].\n\n"
            f"Context:\n{ctx}\n\nQuestion: {question}\n\nAnswer:"
        )
        return prompt

    def generate(self, question: str, contexts: List[Dict], max_tokens: int = 300) -> str:
        prompt = self.build_prompt(question, contexts)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        return response.choices[0].message.content.strip()
