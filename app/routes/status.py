from fastapi import APIRouter

router= APIRouter()

@router.get("/documents/{document_id}/status")
def get_document_status(document_id:str):
    """
    Retrive ingestion status and metadata for a document.
    """
    # Placeholder response for now
    return {
        "document_id":document_id,
        "status":"READY",
        "chunks_indexed":120,
        "vector_db":"pinecone"
    }
    
    