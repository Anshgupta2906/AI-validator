from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import llm_service
from src.models import IdeaInput
from src.rag_pipeline import RAGPipeline
from src.llm_service import LLMService

app = FastAPI(title="AI Idea Validator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag = RAGPipeline()
llm=LLMService()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/validate")
def validate_idea(idea_input: IdeaInput):
    # Create search query
    query = f"{idea_input.idea_name} {idea_input.description}"

    # Retrieve similar examples from Pinecone
    retrieved_chunks = rag.retrieve(query,top_k=3)

    # Score the idea using the retrieved context
    result = llm.score_idea(
        idea_name=idea_input.idea_name,
        idea_description=idea_input.description,
        retrieved_chunks=retrieved_chunks,
        mode=idea_input.mode
    )

    # Return the final result
    return result