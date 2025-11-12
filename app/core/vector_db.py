import os 
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models import ResumeChunk
import json
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()
# Initilize Pinecone

pc=Pinecone(
    api_key=os.getenv("PINECONE_API_KEY") 
)

# create/get index
INDEX_NAME="doc-ingestor"
if INDEX_NAME not in [idx["name"] for idx in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws",region="us-east-1")
        ) # Match embedding size from MiniLM-L6-v2
index= pc.Index(INDEX_NAME)



def store_embeddings(document_id: str, chunks: list, embeddings: list):
    # Pinecone part
    vectors = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vector = {
            "id": f"{document_id}_{i}",
            "values": emb,
            "metadata": {
                "document_id": document_id,
                "chunk_index": i,
                "text": chunk[:500]
            }
        }
        vectors.append(vector)
    index.upsert(vectors)

    # MySQL part
    db: Session = SessionLocal()
    try:
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            record = ResumeChunk(
                document_id=document_id,
                chunk_index=i,
                text=chunk,
                embedding=json.dumps(emb)  # convert list to JSON string
            )
            db.add(record)
        db.commit()
    finally:
        db.close()