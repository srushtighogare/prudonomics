import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from dashboard.style import apply_style
from dashboard.db_utils import get_teams
from backend.pipeline import process_request

st.set_page_config(page_title="Prudonomics", page_icon="", layout="centered")
apply_style()

st.title("Prudonomics Assistant")
st.caption("Ask anything — Prudonomics automatically routes your request to the most cost-appropriate AI model.")

teams_df = get_teams()
team_name_to_id = dict(zip(teams_df["name"], teams_df["id"]))

with st.sidebar:
    st.markdown("### Your Team")
    selected_team_name = st.selectbox("Select your team", list(team_name_to_id.keys()))
    st.write("---")
    st.caption("Prudonomics automatically picks the cheapest model that can handle your request, and blocks usage if your team's budget is exceeded.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="chat-bubble-assistant">', unsafe_allow_html=True)
        st.markdown(msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)
        if msg.get("meta"):
            st.caption(msg["meta"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)

    team_id = team_name_to_id[selected_team_name]
    with st.spinner("Thinking..."):
        result = process_request(team_id, prompt)

    if result["status"] == "blocked_budget":
        response_text = "Sorry, your team's AI budget has been exceeded. Please contact your admin."
        meta = "Blocked by budget policy"
    else:
        response_text = result["response_text"]
        badge = "🔄 fallback used" if result.get("fallback_triggered") else "primary model"
        meta = f"{result['tier']} tier · {result['provider']}/{result['model']} · {badge} · ${result['cost']:.6f}"

    st.session_state.chat_history.append({"role": "assistant", "content": response_text, "meta": meta})
    st.markdown('<div class="chat-bubble-assistant">', unsafe_allow_html=True)
    st.markdown(response_text)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption(meta)