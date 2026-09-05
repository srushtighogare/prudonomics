import sqlite3
import os
from executor import execute_request
from budget_manager import check_budget, add_spend

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "prudonomics.db")

def log_request(team_id, prompt, exec_result) -> int:
    """Logs a request to the requests table. Returns the new request's id."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    model_id = None
    if exec_result["provider"] and exec_result["model"]:
        cur.execute(
            "SELECT id FROM models WHERE provider = ? AND model_name = ?",
            (exec_result["provider"], exec_result["model"])
        )
        row = cur.fetchone()
        model_id = row[0] if row else None

    cur.execute(
        """INSERT INTO requests
           (team_id, prompt, complexity_score, complexity_tier, model_id,
            input_tokens, output_tokens, cost, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (team_id, prompt, exec_result["complexity_score"], exec_result["tier"],
         model_id, exec_result["input_tokens"], exec_result["output_tokens"],
         exec_result["cost"], exec_result["status"])
    )
    request_id = cur.lastrowid
    conn.commit()
    conn.close()
    return request_id

def log_audit(request_id, reasoning, budget_status, fallback_triggered):
    """Logs the audit trail entry explaining the routing decision."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO audit_log
           (request_id, reasoning, budget_status_at_time, fallback_triggered)
           VALUES (?, ?, ?, ?)""",
        (request_id, reasoning, budget_status, int(fallback_triggered))
    )
    conn.commit()
    conn.close()

def process_request(team_id: int, prompt: str) -> dict:
    """
    The full request lifecycle:
    1. Check budget -> block if hard_block
    2. Execute the request (route, call LLM, fallback if needed)
    3. Log the request + audit trail
    4. Update team spend if successful
    """
    budget_status = check_budget(team_id)

    if budget_status["status"] == "hard_block":
        # Log a blocked request WITHOUT calling any LLM -- this costs nothing
        fake_result = {
            "status": "blocked_budget", "tier": None, "complexity_score": None,
            "provider": None, "model": None, "input_tokens": None,
            "output_tokens": None, "cost": None, "response_text": None,
            "fallback_triggered": False,
        }
        request_id = log_request(team_id, prompt, fake_result)
        log_audit(
            request_id,
            reasoning=f"Blocked: team spend ${budget_status['current_spend']:.6f} "
                       f"already at/over budget ${budget_status['budget']:.6f}",
            budget_status=budget_status["status"],
            fallback_triggered=False,
        )
        return {
            "status": "blocked_budget",
            "message": "Request blocked: team budget exceeded.",
            "budget_status": budget_status,
        }

    exec_result = execute_request(prompt)

    request_id = log_request(team_id, prompt, exec_result)
    log_audit(
        request_id,
        reasoning=exec_result["complexity_reasoning"],
        budget_status=budget_status["status"],
        fallback_triggered=exec_result["fallback_triggered"],
    )

    if exec_result["status"] in ("success", "fallback_success") and exec_result["cost"]:
        add_spend(team_id, exec_result["cost"])

    return {
        "status": exec_result["status"],
        "response_text": exec_result["response_text"],
        "tier": exec_result["tier"],
        "provider": exec_result["provider"],
        "model": exec_result["model"],
        "cost": exec_result["cost"],
        "fallback_triggered": exec_result["fallback_triggered"],
        "budget_status": budget_status,
        "request_id": request_id,
    }