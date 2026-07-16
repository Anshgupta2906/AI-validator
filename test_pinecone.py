from src.rag_pipeline import RAGPipeline
pipeline = RAGPipeline()
data=pipeline.load_knowledge_base()


#startups
startups=data["startups"]
startup_chunk=pipeline.chunk_documents(startups)
startup_embeddings=pipeline.embed_chunks(startup_chunk)
result=pipeline.store_in_pinecone(startup_chunk,startup_embeddings,"startup")


#projects
projects=data["projects"]
project_chunk=pipeline.chunk_documents(projects)
project_embeddings=pipeline.embed_chunks(project_chunk)
result=pipeline.store_in_pinecone(project_chunk,project_embeddings,"project")

print(result)