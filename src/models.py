from pydantic import BaseModel
from typing import Optional, Dict, List

class IdeaInput(BaseModel):
    idea_name: str
    description: str
    mode: str  # "startup" or "project"
    additional_context: Optional[str] = None

class Question(BaseModel):
    question_id: int
    text: str

class UserAnswer(BaseModel):
    idea_id: str
    question_id: int
    answer: str

class ScoreBreakdown(BaseModel):
    dimension: str
    score: float
    feedback: str

class ValidationResult(BaseModel):
    idea_name: str
    mode: str
    final_score: float
    rating: str
    dimension_scores: List[ScoreBreakdown]
    action_items: List[str]
    competitive_summary: Optional[str] = None