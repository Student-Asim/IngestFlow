# put chunking functions here
from typing import List
import nltk
from sentence_transformers import SentenceTransformer

nltk.download("punkt") # make sure to donwload the tokenizer once


def chunk_sentence_pack(text:str, sentences_per_chunk:int=5)-> List[str]:
    """split text into chunks of N sentences."""
    sentences= nltk.sent_tokenize(text)
    chunks=[]
    for i in range(0, len(sentences),sentences_per_chunk):
        chunk=" ".join(sentences[i:i+sentences_per_chunk])
        chunks.append(chunk)
    return chunks

def chunk_sliding(text:str, chunk_size:int=500, overlap:int=100)-> List[str]:
    """Split text into sliding window chunks."""
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunks.append(text[start:end])
        start +=chunk_size - overlap
    return chunks

def chunk_text(text:str, strategy:str)->List[str]:
    """Choose chunking strategy."""
    if strategy=="sentence_pack":
        return chunk_sentence_pack(text)
    elif strategy=="sliding":
        return chunk_sliding(text)
    else:
        raise ValueError("Unknown chunking strategy. Choose 'sentence_pack' or sliding.")
    
# embedding function
# load the model once globally for efficiency
embedding_model= SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks: List[str])-> List[List[float]]:
    """Generate embeddings for a list of text chunks using HuggingFace SentenceTransformers."""
    return embedding_model.encode(chunks, convert_to_numpy=True).tolist()
