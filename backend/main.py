from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import process_request

app = FastAPI(title="Prudonomics API")

class RequestPayload(BaseModel):
    team_id: int
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Prudonomics backend is running"}

@app.post("/request")
def handle_request(payload: RequestPayload):
    result = process_request(payload.team_id, payload.prompt)
    return result

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "prudonomics.db")

@app.get("/audit-log/{team_id}")
def get_audit_log(team_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            r.id AS request_id,
            r.prompt,
            r.complexity_score,
            r.complexity_tier,
            r.status,
            r.input_tokens,
            r.output_tokens,
            r.cost,
            r.created_at,
            m.provider,
            m.model_name,
            a.reasoning,
            a.budget_status_at_time,
            a.fallback_triggered
        FROM requests r
        LEFT JOIN models m ON r.model_id = m.id
        LEFT JOIN audit_log a ON a.request_id = r.id
        WHERE r.team_id = ?
        ORDER BY r.created_at DESC
        """,
        (team_id,)
    )
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return {"team_id": team_id, "count": len(rows), "logs": rows}