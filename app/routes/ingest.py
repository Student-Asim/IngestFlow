from fastapi import APIRouter, UploadFile, File, Form
from uuid import uuid4
import uvicorn
from pathlib import Path
import pdfplumber
from core.vector_db import index,store_embeddings
from core.utils import chunk_text, generate_embeddings,embedding_model # import the chunking functions
# from app.core.utils import extract_text # if extract_text is also in utils

router=APIRouter()

UPLOAD_DIR=Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True) #create folder if not exists

def extract_text(file_path: Path) ->str:
    """Extract text form a .txt or .pdf file"""
    if file_path.suffix.lower() ==".txt":
        return file_path.read_text(encoding="utf-8")
    elif file_path.suffix.lower()==".pdf":
        text=""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text= page.extract_text()
                if page_text:
                    text+=page_text+"\n"
        return text
    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf allowed.")

@router.post("/ingest")
async def ingest_documnet(file:UploadFile=File(...),chunk_strategy: str=Form("sentence_pack")):
    """Ingest a document (PDF or txt).
    - file : upload document
    - chunk_strategy: 'sliding' or 'sentence_pack'"""
    document_id= str(uuid4())
    # save uploaded file
    file_path=UPLOAD_DIR / f"{document_id}_{file.filename}"
    with open(file_path,"wb") as f:
        f.write(await file.read())
    # placeholder response for now
    
    # Extract text
    try: 
        text_content= extract_text(file_path)
    except ValueError as e:
        return {"error": str(e)}
    
    # chunk text
    text_content=extract_text(file_path)
    chunks=chunk_text(text_content,chunk_strategy)
    
    # generate embeddings
    embeddings= generate_embeddings(chunks)
    
    # store embeddings
    store_embeddings(document_id,chunks,embeddings)
        
    return {
        
        "document_id":document_id,
        "filename":file.filename,
        "chunk_strategy":chunk_strategy,
        # "status":"TEXT_CHUNKED",
        "status":"EMBEDDINGS_STORED",
        # "text_preview":text_content[:500],# return first 500 chars
        "num_chunks":len(chunks),
        "first_chunk_preview":chunks[0][:300] if chunks else "",
        "embedding_dim":len(embeddings[0]) if embeddings else 0
    }

# when we upload file via Swagger or a client, it will:
# - save the file to uploaded_files/
# return its path in response

@router.post("/query")
async def query_docs(query: str):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).tolist()[0]
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )
    # convert each match's vector to list (if it's a numpy array)
    matches=[]
    for match in results["matches"]:
        matches.append({
            "id":match["id"],
            "score":match["score"],
            "metadata":match.get("metadata",{}),
            "values":list(match["values"]) # ensure vector is list
        })
    return {"matches":matches}
