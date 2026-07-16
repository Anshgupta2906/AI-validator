from statistics import mode

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import json

from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

class RAGPipeline:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def load_knowledge_base(self):
        """Load JSON knowledge base"""
        with open('data/knowledge_base/startup_cases.json', 'r') as file:
            startups = json.load(file)
        
        with open('data/knowledge_base/project_cases.json', 'r') as file:
            projects = json.load(file)

        return {
            "startups": startups,
            "projects": projects
    }


    def chunk_documents(self, documents):
        """Split documents into chunks"""
        chunks = []
        for doc in documents:
            text = f"{doc.get('name', '')} {doc.get('problem', '')} {doc.get('solution', '')} {doc.get('market_size', '')}{doc.get('revenue_model', '')}"
            if text:
                doc_chunks = self.text_splitter.split_text(text)
                chunks.extend(doc_chunks)
        return chunks
    

    
    def embed_chunks(self, chunks):
        """Convert chunks to embeddings"""
        embeddings = self.embedding_model.encode(chunks)
        return embeddings
    


    def store_in_pinecone(self, chunks, embeddings, mode):
        """Store embeddings in Pinecone"""
        from pinecone import Pinecone
        from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
    
    # Initialize Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
    
    # Prepare vectors
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
         vector = (
             f"{mode}_{i}",  # ID
             embedding.tolist(),  # Vector
             {"text": chunk, "mode": mode}  # Metadata
        )
         vectors.append(vector)
         
         index.upsert(vectors=vectors)
        return f"Stored {len(vectors)} vectors in Pinecone"


    def retrieve(self, query, top_k=5):
        """Retrieve relevant chunks for query"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        index=Pinecone(api_key=PINECONE_API_KEY).Index(PINECONE_INDEX_NAME)
        results=index.query(vector=query_embedding.tolist(),
                             top_k=top_k,
                            include_metadata=True)
        retrieved_chunks=[]
        for match in results['matches']:
            retrieved_chunks.append({
                "text": match['metadata']['text'],
                "mode": match['metadata']['mode'],
                "score": match['score']
            })

        return retrieved_chunks