"""LangGraph workflow for the Healthcare Clinic RAG Assistant."""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

try:
    from langgraph.checkpoint.memory import InMemorySaver as Checkpointer
except ImportError:  # Backward compatibility for some LangGraph versions
    from langgraph.checkpoint.memory import MemorySaver as Checkpointer

from .agent import run_agent
from .config import FALLBACK_RESPONSE
from .memory import save_chat_turn
from .safety import is_unsafe_medical_question, safety_response
from .utils import get_latest_human_message


class ClinicAssistantState(TypedDict, total=False):
    """Shared state across LangGraph nodes."""

    messages: Annotated[list[BaseMessage], add_messages]
    thread_id: str
    question: str
    answer: str
    route: str


def receive_question(state: ClinicAssistantState) -> ClinicAssistantState:
    """Extract the latest user question from message history."""
    question = get_latest_human_message(state.get("messages", []))
    return {"question": question, "route": "received"}


def safety_check(state: ClinicAssistantState) -> ClinicAssistantState:
    """Route unsafe medical questions before running RAG."""
    question = state.get("question", "")
    if is_unsafe_medical_question(question):
        return {"route": "unsafe", "answer": safety_response(question)}
    return {"route": "agent"}


def route_after_safety(state: ClinicAssistantState) -> Literal["safety_response", "agent_executor"]:
    return "safety_response" if state.get("route") == "unsafe" else "agent_executor"


def safety_response_node(state: ClinicAssistantState) -> ClinicAssistantState:
    """Return the approved safety response."""
    answer = state.get("answer") or safety_response(state.get("question", ""))
    return {"answer": answer, "route": "unsafe"}


def agent_executor_node(state: ClinicAssistantState) -> ClinicAssistantState:
    """Run the create_agent agent that can call clinic_policy_search."""
    answer = run_agent(state.get("messages", []))
    return {"answer": answer, "route": "agent_completed"}


def check_answer_status(state: ClinicAssistantState) -> ClinicAssistantState:
    """Detect whether agent produced fallback or a grounded answer."""
    answer = state.get("answer", "")
    if FALLBACK_RESPONSE in answer:
        return {"route": "missing", "answer": FALLBACK_RESPONSE}
    return {"route": "found"}


def route_after_answer_check(state: ClinicAssistantState) -> Literal["fallback_response", "save_memory"]:
    return "fallback_response" if state.get("route") == "missing" else "save_memory"


def fallback_response_node(state: ClinicAssistantState) -> ClinicAssistantState:
    """Force exact fallback wording."""
    return {"answer": FALLBACK_RESPONSE, "route": "missing"}


def save_memory_node(state: ClinicAssistantState) -> ClinicAssistantState:
    """Persist conversation turn to a local JSONL file."""
    thread_id = state.get("thread_id", "default")
    save_chat_turn(
        thread_id=thread_id,
        question=state.get("question", ""),
        answer=state.get("answer", ""),
        route=state.get("route", "unknown"),
    )
    return {}


def final_answer_node(state: ClinicAssistantState) -> ClinicAssistantState:
    """Attach the final answer to LangGraph message history."""
    answer = state.get("answer", FALLBACK_RESPONSE)
    return {"messages": [AIMessage(content=answer)]}


def build_graph():
    """Build and compile the LangGraph workflow with memory/checkpointing."""
    builder = StateGraph(ClinicAssistantState)

    builder.add_node("receive_question", receive_question)
    builder.add_node("safety_check", safety_check)
    builder.add_node("safety_response", safety_response_node)
    builder.add_node("agent_executor", agent_executor_node)
    builder.add_node("check_answer_status", check_answer_status)
    builder.add_node("fallback_response", fallback_response_node)
    builder.add_node("save_memory", save_memory_node)
    builder.add_node("final_answer", final_answer_node)

    builder.add_edge(START, "receive_question")
    builder.add_edge("receive_question", "safety_check")
    builder.add_conditional_edges(
        "safety_check",
        route_after_safety,
        {
            "safety_response": "safety_response",
            "agent_executor": "agent_executor",
        },
    )
    builder.add_edge("safety_response", "save_memory")
    builder.add_edge("agent_executor", "check_answer_status")
    builder.add_conditional_edges(
        "check_answer_status",
        route_after_answer_check,
        {
            "fallback_response": "fallback_response",
            "save_memory": "save_memory",
        },
    )
    builder.add_edge("fallback_response", "save_memory")
    builder.add_edge("save_memory", "final_answer")
    builder.add_edge("final_answer", END)

    return builder.compile(checkpointer=Checkpointer())
