from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from database.database import Base

class ResumeChunk(Base):
    __tablename__ = "resume_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(255))
    chunk_index = Column(Integer)
    text = Column(Text)
    embedding = Column(Text)  # store embedding as JSON/text
