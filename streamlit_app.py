"""Streamlit web interface for the Healthcare Clinic RAG Assistant."""

from __future__ import annotations

import uuid

import streamlit as st

from app import run_assistant

st.set_page_config(
    page_title="Healthcare Clinic Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg-start: #f4f8ff;
            --bg-end: #eefbf6;
            --card: rgba(255, 255, 255, 0.84);
            --card-border: rgba(14, 38, 74, 0.10);
            --text-main: #0f172a;
            --text-soft: #475569;
            --accent: #0f766e;
            --accent-2: #2563eb;
            --shadow: 0 24px 70px rgba(15, 23, 42, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.10), transparent 22%),
                linear-gradient(135deg, var(--bg-start) 0%, #fbfdff 45%, var(--bg-end) 100%);
            color: var(--text-main);
        }

        [data-testid="stHeader"] {
            height: 0 !important;
            visibility: hidden;
        }

        [data-testid="stToolbar"] {
            right: 0.75rem;
        }

        .block-container {
            padding-top: 0.35rem;
            padding-bottom: 2rem;
        }

        .hero {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.95), rgba(37, 99, 235, 0.94));
            color: white;
            border-radius: 28px;
            padding: 1.4rem 1.5rem;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 1rem;
        }

        .hero-topline {
            display: flex;
            gap: 0.65rem;
            flex-wrap: wrap;
            margin-bottom: 0.85rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.16);
            border: 1px solid rgba(255, 255, 255, 0.20);
            font-size: 0.86rem;
            font-weight: 600;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2rem, 3.4vw, 3.25rem);
            line-height: 1.05;
            letter-spacing: -0.03em;
        }

        .hero p {
            margin: 0.55rem 0 0;
            max-width: 68ch;
            color: rgba(255, 255, 255, 0.92);
            font-size: 1.02rem;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .hero-card {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            padding: 0.9rem 1rem;
            backdrop-filter: blur(12px);
        }

        .hero-card strong {
            display: block;
            font-size: 0.92rem;
            margin-bottom: 0.25rem;
        }

        .hero-card span {
            color: rgba(255, 255, 255, 0.88);
            font-size: 0.88rem;
            line-height: 1.35;
        }

        .panel {
            background: var(--card);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 1rem 1rem 0.8rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
        }

        .panel + .panel {
            margin-top: 1rem;
        }

        .section-title {
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-soft);
            margin: 0 0 0.65rem;
        }

        [data-testid="stButton"] button {
            width: 100%;
            min-height: 4.3rem;
            border-radius: 18px !important;
            border: 1px solid rgba(37, 99, 235, 0.18) !important;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(244, 248, 255, 0.92)) !important;
            color: var(--text-main) !important;
            box-shadow: 0 10px 28px rgba(37, 99, 235, 0.08);
            font-weight: 600;
            text-align: left;
            padding: 0.75rem 0.85rem !important;
        }

        [data-testid="stButton"] button:hover {
            border-color: rgba(15, 118, 110, 0.45) !important;
            transform: translateY(-1px);
        }

        [data-testid="stChatMessage"] {
            border-radius: 18px;
            padding: 0.15rem 0.1rem;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            line-height: 1.6;
        }

        [data-testid="stChatInput"] {
            border-top: 0;
            padding-top: 0.5rem;
        }

        [data-testid="stChatInput"] textarea {
            border-radius: 18px !important;
            border: 1px solid rgba(15, 23, 42, 0.12) !important;
            background: rgba(255, 255, 255, 0.92) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 25, 41, 0.98), rgba(15, 23, 42, 0.96));
            color: rgba(255, 255, 255, 0.92);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: inherit !important;
        }

        .sidebar-card {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 18px;
            padding: 0.95rem;
        }

        .sidebar-note {
            font-size: 0.92rem;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.82);
        }

        .sidebar-session {
            word-break: break-word;
            font-size: 0.88rem;
            color: rgba(255, 255, 255, 0.72);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{uuid.uuid4()}"

if "messages" not in st.session_state:
    st.session_state.messages = []

starter_questions = [
    "How can I book an appointment?",
    "What time should I arrive before my appointment?",
    "How long should I fast before a fasting blood sugar test?",
    "What should I do in case of a medical emergency?",
]


def ask_starter_question(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching clinic documents..."):
            try:
                answer = run_assistant(question, session_id=st.session_state.session_id)
            except Exception as exc:
                answer = f"Error: {exc}"
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


st.markdown(
    """
    <div class="hero">
        <div class="hero-topline">
            <span class="pill">🏥 Clinic knowledge assistant</span>
            <span class="pill">📄 Answers from your PDF documents</span>
            <span class="pill">🔒 Session-aware chat</span>
        </div>
        <h1>Healthcare Clinic Support Assistant</h1>
        <p>
            A polished, document-grounded chat experience for appointments, lab instructions,
            fees, reports, clinic timings, and emergency guidance.
        </p>
        <div class="hero-grid">
            <div class="hero-card"><strong>Fast answers</strong><span>Ask in plain language and get responses pulled from the clinic documents.</span></div>
            <div class="hero-card"><strong>Safer guidance</strong><span>The assistant stays focused on clinic policy and avoids unrelated medical advice.</span></div>
            <div class="hero-card"><strong>Persistent context</strong><span>Your conversation stays tied to a dedicated session ID during the chat.</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.35, 1], gap="large")

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Suggested prompts</div>', unsafe_allow_html=True)
    starter_columns = st.columns(2)
    for index, prompt in enumerate(starter_questions):
        with starter_columns[index % 2]:
            if st.button(prompt, key=f"starter_{index}", use_container_width=True):
                ask_starter_question(prompt)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Session</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sidebar-session">{st.session_state.session_id}</div>',
        unsafe_allow_html=True,
    )
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = f"streamlit-{uuid.uuid4()}"
        st.rerun()
    st.markdown(
        '<div class="sidebar-note">Before using the app, run:<br><br>'
        'python scripts/download_public_pdfs.py<br>'
        'python app.py --build-index</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height: 0.45rem;"></div>', unsafe_allow_html=True)

chat_area = st.container()
with chat_area:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask about appointments, lab tests, fees, reports, or emergency policy..."
    )

    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Searching clinic documents..."):
                try:
                    answer = run_assistant(user_question, session_id=st.session_state.session_id)
                except Exception as exc:
                    answer = f"Error: {exc}"
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
