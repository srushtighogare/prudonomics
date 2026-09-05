import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "prudonomics.db")

SOFT_ALERT_THRESHOLD = 0.8  # 80% of budget

def get_team(team_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise ValueError(f"No team found with id {team_id}")
    return dict(row)

def check_budget(team_id: int) -> dict:
    """
    Checks a team's current spend against their budget.
    Returns a status: 'ok', 'soft_alert', or 'hard_block'.
    """
    team = get_team(team_id)
    budget = team["monthly_budget"]
    spend = team["current_spend"]
    usage_ratio = spend / budget if budget > 0 else 1.0

    if spend >= budget:
        status = "hard_block"
    elif usage_ratio >= SOFT_ALERT_THRESHOLD:
        status = "soft_alert"
    else:
        status = "ok"

    return {
        "status": status,
        "budget": budget,
        "current_spend": spend,
        "usage_ratio": round(usage_ratio, 3),
    }

def add_spend(team_id: int, cost: float):
    """
    Adds a cost to a team's current_spend after a successful request.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "UPDATE teams SET current_spend = current_spend + ? WHERE id = ?",
        (cost, team_id)
    )
    conn.commit()
    conn.close()