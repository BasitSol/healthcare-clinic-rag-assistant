"""Central configuration for the Healthcare Clinic RAG Assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Environment-driven app settings."""

    model_provider: str = os.getenv("MODEL_PROVIDER", "groq").strip().lower()

    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    docs_dir: Path = Path(os.getenv("DOCS_DIR", "docs"))
    vectorstore_dir: Path = Path(os.getenv("VECTORSTORE_DIR", "vectorstore/faiss_index"))
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("TOP_K", "4"))

    chat_history_path: Path = Path(
        os.getenv("CHAT_HISTORY_PATH", "chat_history/conversations.jsonl")
    )


settings = Settings()


FALLBACK_RESPONSE = (
    "I could not find this information in the provided clinic documents. "
    "Please contact the clinic staff for confirmation."
)

GENERAL_SAFETY_RESPONSE = (
    "I am not a doctor and cannot provide medical diagnosis or treatment advice. "
    "Please consult a qualified healthcare professional."
)

URGENT_SAFETY_RESPONSE = (
    "I am not a doctor and cannot provide medical diagnosis or treatment advice. "
    "Please seek urgent medical help or contact emergency services."
)
