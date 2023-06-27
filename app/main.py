from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from functools import wraps
from datetime import datetime
from typing import Dict
import uvicorn
from mangum import Mangum

from core import pipeline
from pdf_loader import load_btyes_io_api
from preprocessing import load_nltk
from embedding import load_model

app = FastAPI()

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
        return JSONResponse(response)

    return wrap

@app.on_event("startup")
def startup_load():
    """Load the model and nltk packages"""
    load_nltk()
    load_model()
    print('Embedding and nltk packages are ready')
    return

@app.get("/health-check")
@construct_response
def root(request: Request):
    """Heatlh Check"""
    load_nltk()
    load_model()
    response = {
        "message": "Embedding and nltk packages are ready",
        "status-code": HTTPStatus.OK,
        "data": {},
    }   
    return response

@app.post("/resume")
@construct_response
def resume(request: Request, job_description: str, files: list[UploadFile] = File(...)) -> Dict:
    """Endpoint for resume parsing"""
    
    fileArray = load_btyes_io_api(files)
    results, result_pairwise = pipeline(job_description, fileArray)
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": results,
    }   
    return response

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

handler = Mangum(app)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8000)