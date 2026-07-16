from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import IdeaInput

app = FastAPI(title="AI Idea Validator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/validate/init")
def init_validation(idea: IdeaInput):
    return {
        "idea_id": "temp_id",
        "question_id": 1,
        "question_text": "What's your target market?"
    }