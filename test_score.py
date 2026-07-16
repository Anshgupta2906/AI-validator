from src.rag_pipeline import RAGPipeline
from src.llm_service import LLMService

pipeline = RAGPipeline()
llm_service = LLMService()

# User's idea
idea_name = "AI Fitness Coach"
idea_description = "A personalized fitness app using AI to create custom workout plans based on user health data and goals"

# Retrieve similar examples
retrieved = pipeline.retrieve(idea_description, top_k=3)

# Score the idea
result = llm_service.score_idea(idea_name, idea_description, retrieved, "project")

# Print result
import json
print(json.dumps(result, indent=2))