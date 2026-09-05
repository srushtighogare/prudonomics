import streamlit as st
import sys
import os
import altair as alt

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from dashboard.style import apply_style
from dashboard.db_utils import get_teams, get_requests

st.set_page_config(page_title="Prudonomics — Admin", page_icon="📊", layout="wide")
apply_style()

st.title("Prudonomics Admin Dashboard")
st.caption("Cost governance, routing explainability, and budget oversight")

teams_df = get_teams()
requests_df = get_requests()

# --- KPI Cards ---
total_spend = teams_df["current_spend"].sum()
total_requests = len(requests_df)
fallback_count = len(requests_df[requests_df["fallback_triggered"] == 1]) if not requests_df.empty else 0
blocked_count = len(requests_df[requests_df["status"] == "blocked_budget"]) if not requests_df.empty else 0

col1, col2, col3, col4 = st.columns(4)
for col, label, value in zip(
    [col1, col2, col3, col4],
    ["Total Spend", "Total Requests", "Fallbacks Triggered", "Budget Blocks"],
    [f"${total_spend:.4f}", total_requests, fallback_count, blocked_count]
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")
st.write("---")

# --- Charts ---
st.subheader("Spend Breakdown")

st.markdown("**Spend by Team**")
if not teams_df.empty:
    chart1 = alt.Chart(teams_df).mark_bar(color="#6366f1", size=60).encode(
        x=alt.X("name:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("current_spend:Q", title="Spend ($)", scale=alt.Scale(domainMin=0)),
        tooltip=["name", "current_spend"]
    ).properties(height=300)
    st.altair_chart(chart1, use_container_width=True)
else:
    st.info("No team data yet.")

st.write("")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Requests by Tier**")
    if not requests_df.empty and "complexity_tier" in requests_df.columns:
        tier_df = requests_df["complexity_tier"].value_counts().reset_index()
        tier_df.columns = ["tier", "count"]
        chart2 = alt.Chart(tier_df).mark_bar(color="#34d399", size=60).encode(
            x=alt.X("tier:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("count:Q", title="Requests", scale=alt.Scale(domainMin=0)),
            tooltip=["tier", "count"]
        ).properties(height=280)
        st.altair_chart(chart2, use_container_width=True)
    else:
        st.info("No request data yet.")

with col_b:
    st.markdown("**Cost by Provider**")
    if not requests_df.empty and "provider" in requests_df.columns:
        provider_df = requests_df.groupby("provider")["cost"].sum().reset_index()
        chart3 = alt.Chart(provider_df).mark_bar(color="#fbbf24", size=60).encode(
            x=alt.X("provider:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("cost:Q", title="Cost ($)", scale=alt.Scale(domainMin=0)),
            tooltip=["provider", "cost"]
        ).properties(height=280)
        st.altair_chart(chart3, use_container_width=True)
    else:
        st.info("No provider cost data yet.")

st.write("---")

# --- Audit Trail ---
st.subheader("Audit Trail — Every Routing Decision, Explained")

team_options = ["All Teams"] + teams_df["name"].tolist()
selected_team = st.selectbox("Filter by team", team_options)

filtered_df = requests_df if selected_team == "All Teams" else requests_df[requests_df["team_name"] == selected_team]

if filtered_df.empty:
    st.info("No requests logged yet for this selection.")
else:
    for _, row in filtered_df.iterrows():
        status = row["status"]
        status_class = {
            "success": "status-ok",
            "fallback_success": "status-soft_alert",
            "blocked_budget": "status-hard_block",
        }.get(status, "")

        with st.expander(f"[{row['team_name']}] {row['prompt'][:70]}{'...' if len(row['prompt']) > 70 else ''}  —  {row['created_at']}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Status:** <span class='{status_class}'>{status}</span>", unsafe_allow_html=True)
                st.markdown(f"**Tier:** {row['complexity_tier'] or '—'}")
                st.markdown(f"**Complexity score:** {row['complexity_score'] if row['complexity_score'] is not None else '—'}")
            with c2:
                st.markdown(f"**Provider:** {row['provider'] or '—'}")
                st.markdown(f"**Model:** {row['model_name'] or '—'}")
                st.markdown(f"**Fallback triggered:** {'Yes' if row['fallback_triggered'] else 'No'}")
            with c3:
                st.markdown(f"**Cost:** ${row['cost']:.8f}" if row['cost'] is not None else "**Cost:** $0 (blocked)")
                st.markdown(f"**Tokens:** {row['input_tokens'] or 0} in / {row['output_tokens'] or 0} out")
                st.markdown(f"**Budget status at time:** {row['budget_status_at_time'] or '—'}")

            st.markdown("**Why this routing decision was made:**")
            st.code(row["reasoning"] or "No reasoning logged (likely a budget block).", language=None)