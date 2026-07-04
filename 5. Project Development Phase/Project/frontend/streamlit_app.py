"""
Personalized Networking Assistant – Streamlit Frontend
========================================================
A polished, light-themed user interface for the Personalized Networking
Assistant. Lets a user describe an event and their interests, then surfaces
AI-generated conversation starters, a quick fact-checker, and session
history / feedback dashboards.
"""

import json
import sys
from pathlib import Path

import requests
# pyrefly: ignore [missing-import]
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────
# Python path setup — allows importing app.services modules from project root
# ──────────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.services import feedback_logger

# ──────────────────────────────────────────────────────────────────────────
# Backend connection
# ──────────────────────────────────────────────────────────────────────────
try:
    from app.config import BACKEND_URL
except Exception:
    BACKEND_URL = "http://127.0.0.1:8000"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"

# ──────────────────────────────────────────────────────────────────────────
# Force a light theme at the Streamlit-engine level (not just CSS).
# This writes .streamlit/config.toml next to this script on first run, so
# the light theme survives even if the user's OS/browser prefers dark mode.
# Without this, Streamlit's own chrome (toolbar, menus, some native widgets)
# can stay dark no matter what CSS overrides are injected below.
# ──────────────────────────────────────────────────────────────────────────
_STREAMLIT_CONFIG_DIR = Path(__file__).resolve().parent / ".streamlit"
_STREAMLIT_CONFIG_FILE = _STREAMLIT_CONFIG_DIR / "config.toml"
_STREAMLIT_CONFIG_CONTENTS = """[theme]
base = "light"
primaryColor = "#2563EB"
backgroundColor = "#F8FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#0F172A"
font = "sans serif"
"""

try:
    _STREAMLIT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not _STREAMLIT_CONFIG_FILE.exists():
        _STREAMLIT_CONFIG_FILE.write_text(_STREAMLIT_CONFIG_CONTENTS, encoding="utf-8")
except OSError:
    # Non-fatal: if the directory isn't writable (e.g. read-only deployment),
    # the CSS overrides further down still provide a light theme.
    pass


# ──────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────
def find_data_file(filename: str):
    """
    Locate a data file even if the script's working directory or folder
    layout differs from what's expected. Checks the conventional
    `data/<filename>` location relative to this file first, then falls
    back to searching nearby directories.
    """
    candidates = [
        DATA_DIR / filename,
        Path(__file__).resolve().parent / "data" / filename,
        Path(__file__).resolve().parent / filename,
        Path.cwd() / "data" / filename,
        Path.cwd() / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Last resort: search a couple of levels up from this file.
    root = Path(__file__).resolve().parent.parent
    for found in root.rglob(filename):
        return found

    return None


def load_json(path):
    """Safely load a JSON file, returning an empty list if missing/invalid."""
    if path is None or not Path(path).exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def render_badges(items: list[str]) -> str:
    """Render a list of strings as rounded pill badges."""
    return " ".join(
        f'<span style="display:inline-block; background-color:#E0F2FE; color:#0369A1; '
        f'padding:0.3rem 0.8rem; border-radius:9999px; font-size:0.85rem; font-weight:500; '
        f'margin:0 0.4rem 0.4rem 0; border:1px solid #BAE6FD;">{item}</span>'
        for item in items
    )


# ──────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS for a clean, premium light theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ---- Global ---- */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    .stMarkdown p, label, span {
        color: #334155 !important;
    }


    /* ---- Streamlit Top Toolbar Fix ---- */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    header[data-testid="stHeader"] * {
        color: #0F172A !important;
    }

    header[data-testid="stHeader"] button {
        background-color: transparent !important;
        color: #0F172A !important;
        border: none !important;
    }

    header[data-testid="stHeader"] button:hover {
        background-color: #F1F5F9 !important;
    }

    div[data-testid="stMainMenuPopover"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
    }

    div[data-testid="stMainMenuPopover"] * {
        color: #0F172A !important;
    }

    /* ---- Sidebar (force light theme regardless of system/browser theme) ---- */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #0F172A !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: none !important;
    }
    section[data-testid="stSidebar"] code {
        background-color: #F1F5F9 !important;
        color: #0369A1 !important;
        border-radius: 4px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        background-color: #EFF6FF !important;
        color: #1E40AF !important;
    }

    /* ---- Cards (bordered containers) ---- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* ---- Inputs ---- */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #64748B !important;
        opacity: 1 !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2) !important;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0284C7 0%, #1D4ED8 100%) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    }
    .stButton > button[kind="secondary"] {
        background-color: #F1F5F9 !important;
        color: #334155 !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
    }

    /* ---- Metrics ---- */
    div[data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-weight: 700 !important;
    }
    

    /* ---- Final Streamlit Header / Menu / Sidebar Fix ---- */

    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }

    header[data-testid="stHeader"] * {
        color: #0F172A !important;
    }

    header[data-testid="stHeader"] button {
        color: #0F172A !important;
        background-color: transparent !important;
    }

    div[data-testid="stMainMenuPopover"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12) !important;
    }

    div[data-testid="stMainMenuPopover"] * {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
    }

    div[data-testid="stMainMenuPopover"] li:hover {
        background-color: #F1F5F9 !important;
    }

    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #0F172A !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: #0F172A !important;
    }

    section[data-testid="stSidebar"] button {
        color: #0F172A !important;
    }

    section[data-testid="stSidebar"] button svg {
        fill: #0F172A !important;
    }
</style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💡 Quick Tips")
    st.markdown(
        """
        - **Be specific** in your event description to get highly tailored themes.
        - **Separate interests with commas** (e.g. `AI, green energy, sustainability`).
        - Use **Fact Check** to quickly verify topics before initiating a conversation.
        - Browse your **History** to review previously generated starters.
        """
    )

    st.markdown("---")
    st.markdown("### 📋 Sample Events")

    sample_events = load_json(find_data_file("history.json"))
    if sample_events:
        # Show the most recent unique events first
        seen_descriptions = set()
        for ev in reversed(sample_events):
            description = ev.get("description", "Untitled Event")
            if description in seen_descriptions:
                continue
            seen_descriptions.add(description)

            with st.expander(description):
                st.write(f"**Interests:** {', '.join(ev.get('interests', [])) or '—'}")
                st.caption(f"**Themes:** {', '.join(ev.get('topics', [])) or '—'}")
    else:
        st.info("No sample events found yet. Generate some starters to populate this list.")

# ──────────────────────────────────────────────────────────────────────────
# App header
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #E0E7FF 100%);
                padding: 2.2rem; border-radius: 16px; border: 1px solid #BAE6FD; margin-bottom: 2rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
        <h1 style="color: #0369A1; margin: 0; font-size: 2.2rem; font-weight: 700; display: flex; align-items: center; gap: 0.75rem;">
            🤝 Personalized Networking Assistant
        </h1>
        <p style="color: #475569; margin: 0.6rem 0 0 0; font-size: 1.1rem; line-height: 1.5;">
            An AI-powered system designed to generate tailored, context-aware conversation
            starters and real-time fact-checks.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# Section 1 — Generate conversation starters
# ──────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("### 🚀 Generate Starters")

    col_desc, col_int = st.columns([3, 2])
    with col_desc:
        event_description = st.text_area(
            "Event Description",
            placeholder=(
                "e.g. AI for Sustainable Cities – exploring how AI, IoT, and clean "
                "energy reshape modern infrastructure."
            ),
            height=110,
        )
    with col_int:
        user_interests = st.text_area(
            "Your Interests (comma-separated)",
            placeholder="e.g. climate change, smart infrastructure, green energy",
            height=70,
        )

    generate_btn = st.button(
        "Generate Conversation Starters", type="primary", use_container_width=True
    )

    if generate_btn:
        if event_description.strip() and user_interests.strip():
            interests_list = [i.strip() for i in user_interests.split(",") if i.strip()]
            payload = {"description": event_description, "interests": interests_list}

            with st.spinner("Analyzing event themes and generating conversation starters..."):
                try:
                    resp = requests.post(
                        f"{BACKEND_URL}/generate-conversation",
                        json=payload,
                        timeout=120,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state["topics"] = data.get("topics", [])
                        st.session_state["suggestions"] = data.get("suggestions", [])
                        st.session_state["gen_error"] = None
                    else:
                        st.session_state["gen_error"] = (
                            f"Backend returned error code {resp.status_code}."
                        )
                except requests.exceptions.ConnectionError:
                    st.session_state["gen_error"] = (
                        "❌ Could not connect to the backend server. Please verify the "
                        f"FastAPI backend is running on {BACKEND_URL}."
                    )
                except requests.exceptions.Timeout:
                    st.session_state["gen_error"] = (
                        "⏱️ Connection timed out. The local transformer models may still be loading."
                    )
        else:
            st.warning("⚠️ Please provide both the event description and your interests.")

    if st.session_state.get("gen_error"):
        st.error(st.session_state["gen_error"])

    if st.session_state.get("suggestions"):
        st.markdown("---")

        st.write("**Extracted Event Themes:**")
        st.markdown(render_badges(st.session_state.get("topics", [])), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.write("**Suggested Conversation Starters:**")
        for i, suggestion in enumerate(st.session_state["suggestions"]):
            st.markdown(
                f"""
                <div style="background-color:#F8FAFC; border-left:4px solid #0EA5E9;
                            padding:1rem; border-radius:8px; margin-bottom:0.6rem;
                            box-shadow:0 1px 2px rgba(0,0,0,0.02); color:#0F172A; font-weight:500;">
                    {suggestion}
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_like, col_dislike = st.columns([1, 1])
            with col_like:
                if st.button("👍 Useful", key=f"like_{i}", type="secondary", use_container_width=True):
                    feedback_logger.log_feedback(suggestion, "like")
                    st.success("Liked!")
            with col_dislike:
                if st.button("👎 Not Useful", key=f"dislike_{i}", type="secondary", use_container_width=True):
                    feedback_logger.log_feedback(suggestion, "dislike")
                    st.info("Feedback noted.")
            st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Section 2 — Quick fact-check
# ──────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("### 🔍 Fact Verification")

    fact_query = st.text_input(
        "Enter a topic or claim to verify",
        placeholder="e.g. blockchain in healthcare",
        key="fact_query_input",
    )
    fact_btn = st.button("Verify Fact", type="primary")

    if fact_btn:
        if fact_query.strip():
            with st.spinner("Retrieving Wikipedia summary..."):
                try:
                    fc_resp = requests.post(
                        f"{BACKEND_URL}/fact-check",
                        json={"query": fact_query.strip()},
                        timeout=15,
                    )
                    if fc_resp.status_code == 200:
                        summary = fc_resp.json().get("summary", "No summary found.")
                        st.markdown(
                            f"""
                            <div style="background-color:#F0FDF4; border:1px solid #BBF7D0;
                                        padding:1.2rem; border-radius:8px; color:#166534; line-height:1.6;">
                                <strong>Wikipedia Summary:</strong><br>{summary}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("Fact-check API returned an error status.")
                except Exception:
                    st.error("Failed to perform fact check. Please check connection.")
        else:
            st.warning("⚠️ Please enter a topic to verify.")

# ──────────────────────────────────────────────────────────────────────────
# Section 3 — Conversation history
# ──────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("### 📖 Recent Conversation History")
    show_history = st.button("Show Session History", type="secondary")

    if show_history:
        history = load_json(find_data_file("history.json"))
        if history:
            for item in reversed(history[-5:]):
                st.markdown(
                    f"""
                    <div style="background-color:#F8FAFC; border:1px solid #E2E8F0;
                                padding:1rem; border-radius:8px; margin-bottom:0.8rem;">
                        <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:0.4rem;">
                            📅 {item.get('timestamp', 'N/A')}
                        </div>
                        <strong>Event:</strong> {item.get('description', '')}<br>
                        <strong>Interests:</strong> {', '.join(item.get('interests', []))}<br>
                        <strong>Themes:</strong> {', '.join(item.get('topics', []))}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.expander("View generated starters"):
                    for starter in item.get("suggestions", []):
                        st.markdown(f"- {starter}")
        else:
            st.info("No session history found yet.")

# ──────────────────────────────────────────────────────────────────────────
# Section 4 — Feedback log
# ──────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("### 📊 Feedback History & Metrics")
    show_feedback = st.button("Show Feedback Log", type="secondary")

    if show_feedback:
        feedback_data = load_json(find_data_file("feedback.json"))
        if feedback_data:
            likes = sum(1 for e in feedback_data if e.get("feedback") == "like")
            dislikes = sum(1 for e in feedback_data if e.get("feedback") == "dislike")

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Total Ratings", len(feedback_data))
            col_m2.metric("👍 Helpful", likes)
            col_m3.metric("👎 Not Helpful", dislikes)

            st.markdown("**Recent Ratings:**")
            for entry in reversed(feedback_data[-10:]):
                icon = "👍" if entry.get("feedback") == "like" else "👎"
                st.markdown(
                    f"""
                    <div style="background-color:#F8FAFC; border:1px solid #E2E8F0;
                                padding:0.8rem 1rem; border-radius:8px; margin-bottom:0.5rem;
                                display:flex; align-items:center; gap:0.8rem;">
                        <span style="font-size:1.25rem;">{icon}</span>
                        <div>
                            <div style="color:#0F172A; font-weight:500;">{entry.get('suggestion', '')}</div>
                            <div style="font-size:0.75rem; color:#94A3B8; margin-top:0.2rem;">
                                {entry.get('timestamp', '')}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No feedback has been submitted yet.")

# ──────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center; margin-top:2rem; color:#94A3B8; font-size:0.85rem; padding:1rem 0;">
        Personalized Networking Assistant &nbsp;•&nbsp; Built with Streamlit, FastAPI, and Hugging Face Transformers
    </div>
    """,
    unsafe_allow_html=True,
)

