from fastapi import FastAPI

app = FastAPI(title="Prudonomics API")

@app.get("/")
def read_root():
    return {"status": "Prudonomics backend is running"}