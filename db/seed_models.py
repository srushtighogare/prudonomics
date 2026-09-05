import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "prudonomics.db")

MODELS = [
    # provider, model_name, tier, input_price_per_1k, output_price_per_1k
    ("google", "gemini-3.1-flash-lite", "cheap", 0.00025, 0.0015),
    ("google", "gemini-3.1-pro", "premium", 0.002, 0.012),
    ("groq", "llama-3.1-8b-instant", "cheap", 0.00005, 0.00008),
    ("groq", "llama-3.3-70b-versatile", "premium", 0.00059, 0.00079),
]

def seed_models():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM models")  # clear existing rows if re-run
    cur.executemany(
        "INSERT INTO models (provider, model_name, tier, input_price_per_1k, output_price_per_1k) VALUES (?, ?, ?, ?, ?)",
        MODELS
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(MODELS)} models into the database")

if __name__ == "__main__":
    seed_models()