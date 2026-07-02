"""Agent tools for clinic document retrieval."""

from __future__ import annotations

import re
from functools import lru_cache

from langchain_core.tools import tool

from .config import settings
from .vector_store import load_vector_store

CLINIC_POLICY_SEARCH_DESCRIPTION = (
    "Use this tool to search healthcare clinic policies about appointments, "
    "doctor schedules, lab tests, fees, medicine refills, emergencies, and report collection."
)

NO_RELEVANT_CONTEXT = "NO_RELEVANT_CONTEXT_FOUND"

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "is", "are", "was", "were",
    "do", "does", "did", "can", "could", "should", "would", "i", "me", "my", "you",
    "your", "we", "our", "they", "their", "to", "for", "of", "in", "on", "at", "by",
    "with", "from", "this", "that", "it", "as", "be", "been", "being", "what", "how",
    "when", "where", "who", "why", "before", "after", "while", "about", "clinic",
    "patient", "patients", "information", "please", "need", "provide", "tell", "ask",
}


@lru_cache(maxsize=1)
def _get_vector_store():
    return load_vector_store()


def _terms(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", text.lower())
    return {word for word in words if word not in STOPWORDS}


def _has_minimum_overlap(query: str, context: str) -> bool:
    """Light lexical gate to avoid answering from irrelevant retrieval."""
    query_terms = _terms(query)
    if not query_terms:
        return True

    context_terms = _terms(context)
    overlap = query_terms.intersection(context_terms)

    # For short follow-up questions, allow the LLM to use conversation history.
    if len(query_terms) <= 2:
        return True

    return len(overlap) >= 1


@tool("clinic_policy_search", description=CLINIC_POLICY_SEARCH_DESCRIPTION)
def clinic_policy_search(query: str) -> str:
    """Search clinic PDF documents and return grounded context with sources."""
    vector_store = _get_vector_store()
    docs = vector_store.similarity_search(query, k=settings.top_k)

    if not docs:
        return NO_RELEVANT_CONTEXT

    context_blocks: list[str] = []
    merged_context = "\n".join(doc.page_content for doc in docs)

    if not _has_minimum_overlap(query, merged_context):
        return NO_RELEVANT_CONTEXT

    for rank, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown_source")
        page = doc.metadata.get("page", "unknown_page")
        content = " ".join(doc.page_content.split())
        context_blocks.append(
            f"[Retrieved chunk {rank}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {content}"
        )

    return "\n\n".join(context_blocks)


TOOLS = [clinic_policy_search]
