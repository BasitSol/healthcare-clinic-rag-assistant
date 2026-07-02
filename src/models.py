"""LLM provider factory for Groq or Gemini."""

from __future__ import annotations

import os

from langchain_core.language_models.chat_models import BaseChatModel

from .config import settings


def get_chat_model() -> BaseChatModel:
    """Return the configured chat model.

    Supported providers:
    - MODEL_PROVIDER=groq
    - MODEL_PROVIDER=gemini
    """
    provider = settings.model_provider

    if provider == "groq":
        if not settings.groq_api_key or settings.groq_api_key.startswith("your_"):
            raise EnvironmentError(
                "GROQ_API_KEY is missing. Add it to .env or set MODEL_PROVIDER=gemini."
            )
        os.environ["GROQ_API_KEY"] = settings.groq_api_key
        from langchain_groq import ChatGroq

        return ChatGroq(model=settings.groq_model, temperature=0)

    if provider == "gemini":
        if not settings.google_api_key or settings.google_api_key.startswith("your_"):
            raise EnvironmentError(
                "GOOGLE_API_KEY is missing. Add it to .env or set MODEL_PROVIDER=groq."
            )
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=settings.gemini_model, temperature=0)

    raise ValueError("MODEL_PROVIDER must be either 'groq' or 'gemini'.")
