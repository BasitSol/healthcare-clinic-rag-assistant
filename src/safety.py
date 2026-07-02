"""Simple healthcare safety guardrails.

This is not a medical classifier. It is a practical rule-based safety layer for
an academic clinic-policy assistant. The goal is to block diagnosis/treatment
advice while still allowing clinic policy questions.
"""

from __future__ import annotations

import re

from .config import GENERAL_SAFETY_RESPONSE, URGENT_SAFETY_RESPONSE

EMERGENCY_SYMPTOMS = {
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "unconscious",
    "severe bleeding",
    "stroke",
    "heart attack",
    "poisoning",
    "seizure",
    "can not breathe",
    "can't breathe",
}

TREATMENT_REQUEST_PATTERNS = [
    r"\bwhat medicine\b",
    r"\bwhich medicine\b",
    r"\bwhat drug\b",
    r"\bwhich drug\b",
    r"\bwhat dose\b",
    r"\bdosage\b",
    r"\bcan i take\b",
    r"\bshould i take\b",
    r"\bprescribe\b",
    r"\btreat\b",
    r"\bdiagnose\b",
    r"\bantibiotic\b",
    r"\bpainkiller\b",
]

POLICY_ALLOWLIST_PATTERNS = [
    r"clinic policy",
    r"emergency policy",
    r"in case of (a )?medical emergency",
    r"what should i do in case of (a )?medical emergency",
    r"clinic emergency",
]


def _contains_any(text: str, phrases: set[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def is_policy_question(text: str) -> bool:
    normalized = text.lower()
    return any(re.search(pattern, normalized) for pattern in POLICY_ALLOWLIST_PATTERNS)


def is_unsafe_medical_question(text: str) -> bool:
    """Return True when user asks for diagnosis/treatment instead of policy info."""
    normalized = text.lower().strip()

    if is_policy_question(normalized):
        return False

    has_treatment_request = any(
        re.search(pattern, normalized) for pattern in TREATMENT_REQUEST_PATTERNS
    )
    has_emergency_symptom = _contains_any(normalized, EMERGENCY_SYMPTOMS)

    return bool(has_treatment_request or (has_emergency_symptom and "medicine" in normalized))


def safety_response(text: str) -> str:
    normalized = text.lower().strip()
    if _contains_any(normalized, EMERGENCY_SYMPTOMS):
        return URGENT_SAFETY_RESPONSE
    return GENERAL_SAFETY_RESPONSE
