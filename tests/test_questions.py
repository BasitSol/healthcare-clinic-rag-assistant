"""Manual test runner for the Healthcare Clinic RAG Assistant.

Run from project root:
    python tests/test_questions.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import BONUS_TEST_QUESTIONS, REQUIRED_TEST_QUESTIONS, run_assistant


def main() -> None:
    session_id = "test-session"
    print("Required tests")
    print("=" * 80)
    for question in REQUIRED_TEST_QUESTIONS:
        print(f"Q: {question}")
        print(f"A: {run_assistant(question, session_id=session_id)}")
        print("-" * 80)

    print("Bonus tests")
    print("=" * 80)
    for question in BONUS_TEST_QUESTIONS:
        print(f"Q: {question}")
        print(f"A: {run_assistant(question, session_id=session_id)}")
        print("-" * 80)


if __name__ == "__main__":
    main()
