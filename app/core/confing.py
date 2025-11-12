# for later
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    VECTOR_DB_API_KEY=os.getenv("PINECONE_API_KEY")
    DATABASE_URL=os.getenv("DATABASE_URL")
    
settings=Settings()