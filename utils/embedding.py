import os
import google.generativeai as genai
from google.generativeai import types

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str, task_type="RETRIEVAL_QUERY") -> list:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type=task_type  # "RETRIEVAL_QUERY" or "RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]