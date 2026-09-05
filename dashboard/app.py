import streamlit as st
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "prudonomics.db")

st.set_page_config(page_title="Prudonomics", layout="wide")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_teams():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM teams", conn)
    conn.close()
    return df

def get_requests(team_id=None):
    conn = get_connection()
    query = """
        SELECT
            r.id, r.prompt, r.complexity_score, r.complexity_tier,
            r.status, r.input_tokens, r.output_tokens, r.cost, r.created_at,
            m.provider, m.model_name,
            a.reasoning, a.budget_status_at_time, a.fallback_triggered,
            t.name AS team_name
        FROM requests r
        LEFT JOIN models m ON r.model_id = m.id
        LEFT JOIN audit_log a ON a.request_id = r.id
        LEFT JOIN teams t ON r.team_id = t.id
    """
    if team_id:
        query += " WHERE r.team_id = ?"
        df = pd.read_sql_query(query + " ORDER BY r.created_at DESC", conn, params=(team_id,))
    else:
        df = pd.read_sql_query(query + " ORDER BY r.created_at DESC", conn)
    conn.close()
    return df

st.title("💰 Prudonomics")
st.caption("Cost-optimal LLM routing and budget governance")

st.write("Dashboard scaffold loaded successfully.")
st.write("Teams in database:")
st.dataframe(get_teams())