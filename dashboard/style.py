import streamlit as st

def apply_style():
    st.markdown("""
    <style>
        .main { background-color: #0f1117; }

        .metric-card {
            background: linear-gradient(145deg, #1a1d2e, #15171f);
            border: 1px solid #2a2e3e;
            border-radius: 14px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        }
        .metric-label {
            color: #9098b0;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        .metric-value {
            color: #ffffff;
            font-size: 34px;
            font-weight: 800;
            margin-top: 6px;
            background: linear-gradient(90deg, #818cf8, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-ok { color: #34d399; font-weight: 700; }
        .status-soft_alert { color: #fbbf24; font-weight: 700; }
        .status-hard_block { color: #f87171; font-weight: 700; }

        h1 { font-weight: 800; letter-spacing: -0.5px; }
        h2, h3 { font-weight: 700; }

        .stTabs [data-baseweb="tab-list"] { gap: 24px; }

        [data-testid="stExpander"] {
            background-color: #161925;
            border: 1px solid #262a3a;
            border-radius: 10px;
        }

        .stButton button, .stFormSubmitButton button {
            background: linear-gradient(90deg, #6366f1, #3b82f6);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
        }

        .chat-bubble-user {
            background-color: #2563eb;
            color: white;
            padding: 12px 16px;
            border-radius: 16px 16px 4px 16px;
            margin: 8px 0;
            max-width: 75%;
            margin-left: auto;
        }
        .chat-bubble-assistant {
            background-color: #1e2130;
            color: #e5e7eb;
            padding: 12px 16px;
            border-radius: 16px 16px 16px 4px;
            margin: 8px 0;
            max-width: 75%;
            border: 1px solid #2a2e3e;
        }
    </style>
    """, unsafe_allow_html=True)