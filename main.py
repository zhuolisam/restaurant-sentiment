from fastapi import FastAPI, File, UploadFile
from core import pipeline
from pdf_loader import load_btyes_io_api

app = FastAPI()

@app.get("/")
@app.get("/health-check")
async def root():
    return {"message": "Hello World"}


@app.post("/resume")
async def root(job_description: str, files: list[UploadFile] = File(...)):
    fileArray = await load_btyes_io_api(files)
    results, result_pairwise = pipeline(job_description, fileArray)
    return {"results": results}
