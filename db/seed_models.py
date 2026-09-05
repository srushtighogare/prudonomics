import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "prudonomics.db")

MODELS = [
    ("google", "gemini-3.1-flash-lite", "cheap", 0.00025, 0.0015),
    ("google", "gemini-3.5-flash", "premium", 0.0015, 0.009),
    ("groq", "openai/gpt-oss-20b", "cheap", 0.000075, 0.0003),
    ("groq", "openai/gpt-oss-120b", "premium", 0.00015, 0.0006),
]

def seed_models():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM models")  
    cur.executemany(
        "INSERT INTO models (provider, model_name, tier, input_price_per_1k, output_price_per_1k) VALUES (?, ?, ?, ?, ?)",
        MODELS
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(MODELS)} models into the database")

if __name__ == "__main__":
    seed_models()