import os
from collections import Counter
from datetime import datetime

import streamlit as st

from src.response_engine import ResponseEngine
from utils.config import (
    APP_ICON,
    APP_TITLE,
    BOT_NAME,
    COLLEGE_NAME,
    MAX_SUGGESTIONS,
)

# MUST be first Streamlit command
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)


def inject_css() -> None:
    st.markdown(
        """
        <style>

        .stApp {
            background: #ffffff;
        }

        .confidence-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 999px;
            margin-top: 6px;
            border: 1px solid rgba(0,0,0,0.07);
        }

        .confidence-green {
            background: rgba(16,185,129,0.15);
            color: #047857;
            border-color: rgba(16,185,129,0.25);
        }

        .confidence-orange {
            background: rgba(245,158,11,0.16);
            color: #92400e;
            border-color: rgba(245,158,11,0.25);
        }

        .confidence-red {
            background: rgba(239,68,68,0.14);
            color: #991b1b;
            border-color: rgba(239,68,68,0.25);
        }

        .sidebar-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_session_state() -> None:

    if "engine" not in st.session_state:
        st.session_state.engine = ResponseEngine()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "draft_input" not in st.session_state:
        st.session_state["draft_input"] = ""


def render_message(msg: dict) -> None:

    user_message = msg.get("user_message", "")

    bot_response = msg.get("bot_response", "")

    timestamp = msg.get(
        "timestamp",
        datetime.now().strftime("%H:%M")
    )

    confidence_percent = msg.get(
        "confidence_percent",
        ""
    )

    confidence_color = msg.get(
        "confidence_color",
        "orange"
    )

    # USER MESSAGE
    with st.chat_message("user"):

        st.write(user_message)

        st.caption(timestamp)

    # BOT MESSAGE
    with st.chat_message("assistant"):

        st.write(bot_response)

        st.caption(timestamp)

        color_class = {
            "green": "confidence-green",
            "orange": "confidence-orange",
            "red": "confidence-red",
        }.get(confidence_color, "confidence-orange")

        st.markdown(
            f"""
            <div class="confidence-badge {color_class}">
                Confidence: {confidence_percent}
            </div>
            """,
            unsafe_allow_html=True,
        )


def compute_most_asked_topic(messages: list[dict]) -> str:

    intents = [
        m.get("intent")
        for m in messages
        if m.get("intent")
    ]

    if not intents:
        return "N/A"

    return Counter(intents).most_common(1)[0][0]


def format_chat_history_for_download(
    messages: list[dict]
) -> str:

    lines = []

    lines.append(
        "College Inquiry Chatbot - Chat History"
    )

    lines.append("=" * 50)

    lines.append("")

    for i, m in enumerate(messages, start=1):

        ts = m.get("timestamp", "")

        lines.append(f"[{i}] ({ts})")

        lines.append(
            f"You: {m.get('user_message', '')}"
        )

        lines.append(
            f"{BOT_NAME}: {m.get('bot_response', '')}"
        )

        lines.append(
            f"Intent: {m.get('intent', '')}"
        )

        lines.append(
            f"Confidence: {m.get('confidence_percent', '')}"
        )

        lines.append("-" * 50)

    return "\n".join(lines)


def main() -> None:

    inject_css()

    ensure_session_state()

    engine: ResponseEngine = (
        st.session_state.engine
    )

    # Sync chat history
    st.session_state.messages = (
        engine.get_chat_history()
    )

    # SIDEBAR
    with st.sidebar:

        assets_dir = os.path.join(
            os.path.dirname(__file__),
            "assets"
        )

        logo_path = os.path.join(
            assets_dir,
            "college_logo.png"
        )

        if os.path.exists(logo_path):

            st.image(
                logo_path,
                use_container_width=True
            )

        else:
            st.markdown("# 🎓")

        st.markdown(
            '<div class="sidebar-title">About</div>',
            unsafe_allow_html=True
        )

        st.write(
            f"""
            **{BOT_NAME}** helps students with:

            - Admissions
            - Exams
            - Fees
            - Placements
            - Hostel queries
            - Attendance rules
            """
        )

        st.subheader("Suggested Questions")

        suggested_questions = (
            engine.get_suggested_questions()
        )

        for q in suggested_questions[:7]:

            key = f"suggested_{abs(hash(q))}"

            if st.button(q, key=key):

                st.session_state[
                    "draft_input"
                ] = q

        st.subheader("Chat Statistics")

        total_messages = len(
            st.session_state.messages
        )

        most_asked = compute_most_asked_topic(
            st.session_state.messages
        )

        st.metric(
            "Total Messages",
            total_messages
        )

        st.write(
            f"**Most Asked Topic:** `{most_asked}`"
        )

        # CLEAR CHAT
        if st.button("🧹 Clear Chat"):

            engine.clear_history()

            st.session_state.messages = []

            st.session_state["draft_input"] = ""

            st.rerun()

        # DOWNLOAD CHAT
        st.subheader("Export Chat")

        txt = format_chat_history_for_download(
            st.session_state.messages
        )

        st.download_button(
            label="⬇️ Download Chat History",
            data=txt.encode("utf-8"),
            file_name="chat_history.txt",
            mime="text/plain",
        )

    # MAIN TITLE
    st.title(f"{APP_ICON} {APP_TITLE}")

    st.caption(
        f"""
        Ask questions about **{COLLEGE_NAME}**
        including admissions, fees, exams,
        hostel, placements, and attendance.
        """
    )

    # CHAT AREA
    for m in st.session_state.messages:

        render_message(m)

    # CHAT INPUT
    user_input = st.chat_input(
        "Type your question here..."
    )

    if user_input:

        engine.get_response(user_input)

        st.session_state.messages = (
            engine.get_chat_history()
        )

        st.rerun()

    # FOLLOW-UP SUGGESTIONS
    latest = (
        st.session_state.messages[-1]
        if st.session_state.messages
        else None
    )

    if latest:

        followups = latest.get(
            "followup_suggestions",
            []
        )[:MAX_SUGGESTIONS]

        if followups:

            st.subheader(
                "Suggested Follow-up Questions"
            )

            cols = st.columns(len(followups))

            for idx, suggestion in enumerate(
                followups
            ):

                with cols[idx]:

                    if st.button(
                        suggestion,
                        key=f"followup_{idx}"
                    ):

                        engine.get_response(
                            suggestion
                        )

                        st.session_state.messages = (
                            engine.get_chat_history()
                        )

                        st.rerun()


if __name__ == "__main__":
    main()