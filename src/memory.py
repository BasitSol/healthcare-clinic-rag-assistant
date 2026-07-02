"""Local chat history persistence for bonus task."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from .config import settings


def save_chat_turn(thread_id: str, question: str, answer: str, route: str) -> None:
    """Append a chat turn to a local JSONL file."""
    path = settings.chat_history_path
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "thread_id": thread_id,
        "question": question,
        "answer": answer,
        "route": route,
    }

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
