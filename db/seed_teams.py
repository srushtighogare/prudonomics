import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "prudonomics.db")

TEAMS = [
    # name, monthly_budget
    ("engineering", 5.00),
    ("marketing", 0.0002),  # deliberately tiny budget to easily trigger alerts/blocks in testing
]

def seed_teams():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM teams")
    cur.executemany(
        "INSERT INTO teams (name, monthly_budget, current_spend) VALUES (?, ?, 0.0)",
        TEAMS
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(TEAMS)} teams into the database")

if __name__ == "__main__":
    seed_teams()