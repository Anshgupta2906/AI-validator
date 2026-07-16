import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "gcp-starter")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ai-validator")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

LLM_MODEL = "openai/gpt-3.5-turbo"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

STARTUP_WEIGHTS = {
    "market_size": 0.20,
    "problem_fit": 0.15,
    "competition": 0.15,
    "team_feasibility": 0.15,
    "revenue_model": 0.15,
    "go_to_market": 0.10,
    "timing": 0.10,
}

PROJECT_WEIGHTS = {
    "industry_relevance": 0.20,
    "technical_depth": 0.20,
    "differentiation": 0.15,
    "skill_alignment": 0.15,
    "execution_feasibility": 0.15,
    "placement_utility": 0.10,
    "scope_polish": 0.05,
}