from fastapi import FastAPI, File, UploadFile, Request
from http import HTTPStatus
from sentence_transformers import SentenceTransformer
from functools import wraps
from datetime import datetime
from typing import Dict
import nltk
import os

from core import pipeline
from pdf_loader import load_btyes_io_api
app = FastAPI()

@app.on_event("startup")
def load_model():
    """Load the model and nltk packages"""
    download_path = os.path.join(os.getcwd(), 'nltk_packages')
    nltk.data.path.append(download_path)
    nltk.download('wordnet', download_dir=download_path)
    nltk.download('stopwords', download_dir=download_path)
    nltk.download('punkt', download_dir=download_path)
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens', cache_folder=os.path.join(os.getcwd(), 'embedding'))
    print('Model is ready')

@app.get("/health-check")
async def root():
    """Heatlh Check"""
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens', cache_folder=os.path.join(os.getcwd(), 'embedding'))
    return {"message": "Model is ready"}


@app.post("/resume")
async def root(job_description: str, files: list[UploadFile] = File(...)) -> Dict:
    """Endpoint for resume parsing"""
    
    fileArray = await load_btyes_io_api(files)
    results, result_pairwise = pipeline(job_description, fileArray)
    return {"results": results}

def construct_response(f):
    """Construct a JSON response for an endpoint."""

    @wraps(f)
    def wrap(request: Request, *args, **kwargs) -> Dict:
        results = f(request, *args, **kwargs)
        response = {
            "message": results["message"],
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }
        if "data" in results:
            response["data"] = results["data"]
        return response

    return wrap


@app.get("/")
@construct_response
def _index(request: Request) -> Dict:
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response