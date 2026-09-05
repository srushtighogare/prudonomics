import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "prudonomics.db")

def get_model_pricing(provider: str, model_name: str) -> dict:
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM models WHERE provider = ? AND model_name = ?",
        (provider, model_name)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        raise ValueError(f"No pricing found for {provider}/{model_name}")

    return dict(row)

def calculate_cost(provider: str, model_name: str, input_tokens: int, output_tokens: int) -> float:
    
    pricing = get_model_pricing(provider, model_name)
    input_cost = (input_tokens / 1000) * pricing["input_price_per_1k"]
    output_cost = (output_tokens / 1000) * pricing["output_price_per_1k"]
    total_cost = input_cost + output_cost
    return round(total_cost, 8)