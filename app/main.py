from fastapi import FastAPI
from app.routes import ingest, status  # relative import
from database.database import Base, engine
from database.models import ResumeChunk
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="DocIngestor API",
    version="1.0",
    description="Document ingestion backend."
)

app.include_router(ingest.router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(status.router, prefix="/api/v1", tags=["Status"])

@app.get("/")
def root():
    return {"message": "Welcome to DocIngestor API"}

