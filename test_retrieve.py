from src.rag_pipeline import RAGPipeline
pipeline = RAGPipeline()


query="Robotics in healthcare"
results=pipeline.retrieve(query,top_k=5)

print(f"Query: {query}")
print(f"results found: {len(results)}\n")

for i, result in enumerate(results):
    print(f"Result {i+1}:")
    print(f"Text: {result['text'][:100]}...")
    print(f"Mode: {result['mode']}")
    print(f"Score: {result['score']:.3f}\n")


