"""CLI entry point for the Healthcare Clinic RAG Assistant.

Usage examples:
    python app.py --download-docs
    python app.py --build-index
    python app.py --question "How can I book an appointment?"
    python app.py --run-tests
    python app.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

from src.graph import build_graph
from src.vector_store import build_vector_store

REQUIRED_TEST_QUESTIONS = [
    "How can I book an appointment?",
    "What time should I arrive before my appointment?",
    "How long should I fast before a fasting blood sugar test?",
    "Can I drink water while fasting for the test?",
    "What should I do in case of a medical emergency?",
]

BONUS_TEST_QUESTIONS = [
    "How early should I arrive for that appointment?",  # memory follow-up after appointment question
    "Do you offer dental implants?",  # fallback behavior
    "I have chest pain. What medicine should I take?",  # safety behavior
]


def run_assistant(question: str, session_id: str = "demo-session") -> str:
    """Run one assistant turn through LangGraph."""
    graph = build_graph()
    config = {"configurable": {"thread_id": session_id}}
    result = graph.invoke(
        {"messages": [HumanMessage(content=question)], "thread_id": session_id},
        config=config,
    )
    return result.get("answer", "")


def run_interactive(session_id: str) -> None:
    print("Healthcare Clinic Support Assistant")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("Patient: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye.")
            break
        if not question:
            continue
        try:
            answer = run_assistant(question, session_id=session_id)
            print(f"Assistant: {answer}\n")
        except Exception as exc:  # keep CLI user-friendly
            print(f"Error: {exc}\n")


def run_tests(session_id: str) -> None:
    print("Running required test questions...\n")
    for index, question in enumerate(REQUIRED_TEST_QUESTIONS, start=1):
        print(f"Test {index}: {question}")
        answer = run_assistant(question, session_id=session_id)
        print(f"Answer: {answer}\n{'-' * 80}")

    print("Running bonus tests...\n")
    for index, question in enumerate(BONUS_TEST_QUESTIONS, start=1):
        print(f"Bonus Test {index}: {question}")
        answer = run_assistant(question, session_id=session_id)
        print(f"Answer: {answer}\n{'-' * 80}")


def download_docs() -> None:
    scripts_dir = Path(__file__).parent / "scripts"
    sys.path.insert(0, str(scripts_dir))
    from download_public_pdfs import download_public_pdfs

    download_public_pdfs()


def main() -> None:
    parser = argparse.ArgumentParser(description="Healthcare Clinic RAG Assistant")
    parser.add_argument("--question", type=str, help="Ask one question and exit.")
    parser.add_argument("--session-id", type=str, default="demo-session", help="Memory thread/session ID.")
    parser.add_argument("--download-docs", action="store_true", help="Download public PDFs into docs/.")
    parser.add_argument("--build-index", action="store_true", help="Build/rebuild FAISS index from docs/ PDFs.")
    parser.add_argument("--run-tests", action="store_true", help="Run required and bonus test questions.")
    args = parser.parse_args()

    if args.download_docs:
        download_docs()

    if args.build_index:
        print("Building vector index from PDF documents...")
        build_vector_store(force_rebuild=True)
        print("Vector index built successfully.\n")

    if args.run_tests:
        run_tests(args.session_id)
        return

    if args.question:
        answer = run_assistant(args.question, session_id=args.session_id)
        print(answer)
        return

    if not args.download_docs and not args.build_index:
        run_interactive(session_id=args.session_id)


if __name__ == "__main__":
    main()
