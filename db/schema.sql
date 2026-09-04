-- Teams table: tracks each team's budget
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    monthly_budget REAL NOT NULL,
    current_spend REAL NOT NULL DEFAULT 0.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Models table: pricing per model we route to
CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    tier TEXT NOT NULL,
    input_price_per_1k REAL NOT NULL,
    output_price_per_1k REAL NOT NULL
);

-- Requests table: every request that comes through the system
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    complexity_score REAL,
    complexity_tier TEXT,
    model_id INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost REAL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- Audit log table: explains why each request was routed the way it was
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    reasoning TEXT NOT NULL,
    budget_status_at_time TEXT,
    fallback_triggered INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);