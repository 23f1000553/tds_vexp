from fastapi import FastAPI, Request, jsonify
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

@app.get("/")
def index():
    return {"message": "Welcome to the API!"}

@app.get("/api/params")
def get_params(request: Request):
    parameters = list()

    for param_key in request.query_params.keys():
        for param_value in request.query_params.getlist(param_key):
            parameters.append({
                "key": param_key,
                "value": param_value
            })
    print(parameters)
    return parameters


from pydantic import BaseModel
class Job(BaseModel):
    name: str
    description: str
    status: str = "pending"  # Default status is 'pending'

jobs = []
@app.post("/api/create")
def create_job(job: Job):
    jobs.append(job)
    return {"jobs": jobs}

@app.get("/api/jobs")
def get_jobs():
    return {"jobs": jobs}

@app.delete("/api/jobs/{job_no}")
def delete_job(job_no: int):
    if 0 <= job_no < len(jobs):
        deleted_job = jobs.pop(job_no)
        return {"message": "Job deleted successfully", "job": deleted_job}
    else:
        return {"message": "Job not found"}, 404
    
import json

with open("q-vercel-python.json", "r") as file:
    data = json.load(file)

marks_dict = {entry["name"]: entry["marks"] for entry in data}

@app.get("/api")
def get_marks(request: Request):
    parameters = list()

    for param_key in request.query_params.keys():
        for param_value in request.query_params.getlist(param_key):
            parameters.append({
                "key": param_key,
                "value": param_value
            })
    
    
    # Filter marks based on parameters
    filtered_marks = {k: v for k, v in marks_dict.items() if all(param["value"] in v for param in parameters)}
    
    return {"marks": filtered_marks}

