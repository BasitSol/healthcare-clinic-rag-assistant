"""Utility helpers."""

from __future__ import annotations

from typing import Any, Iterable

from langchain_core.messages import BaseMessage, HumanMessage


def normalize_content(content: Any) -> str:
    """Convert LangChain model content into a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                elif "content" in item:
                    parts.append(str(item["content"]))
                else:
                    parts.append(str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    return str(content)


def get_latest_human_message(messages: Iterable[BaseMessage]) -> str:
    """Return the latest human/user message from a message list."""
    for message in reversed(list(messages)):
        if isinstance(message, HumanMessage) or getattr(message, "type", None) == "human":
            return normalize_content(message.content)
    return ""
