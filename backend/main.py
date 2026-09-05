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