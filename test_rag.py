from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
data = pipeline.load_knowledge_base()

print(f"Startups: {len(data['startups'])}")
print(f"Projects: {len(data['projects'])}")