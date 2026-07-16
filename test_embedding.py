from src.rag_pipeline import RAGPipeline
pipeline = RAGPipeline()
data=pipeline.load_knowledge_base()

#startup
startups=data["startups"]
startup_chunk=pipeline.chunk_documents(startups)
startup_embeddings=pipeline.embed_chunks(startup_chunk)

#projects
projects=data["projects"]
project_chunk=pipeline.chunk_documents(projects)
project_embeddings=pipeline.embed_chunks(project_chunk)


print(f"startup chunks:{len(startup_chunk)},embeddings:{len(startup_embeddings)}")
print(f"project chunks:{len(project_chunk)},embeddings:{len(project_embeddings)}")
print(f"Embedding dimensions: {len(startup_embeddings[0])}")