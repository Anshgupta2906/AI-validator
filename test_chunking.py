from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
data=pipeline.load_knowledge_base()

#STARTUP
startup=data['startups']
startup_chunks=pipeline.chunk_documents(startup)

#project
project=data['projects']
project_chunks=pipeline.chunk_documents(project)


print(f"Total Project Chunks: {len(project_chunks)}")
print(f"First Project Chunk:\n{project_chunks[0]}")

