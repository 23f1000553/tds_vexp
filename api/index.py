from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Welcome to the API!"}

with open("q-vercel-python.json", "r") as file:
    data = json.load(file)

marks_dict = {entry["name"]: entry["marks"] for entry in data}

@app.get("/api")
async def get_params(request: Request):  # ✅ async & correct injection
    parameters = []

    for param_key in request.query_params.keys():
        for param_value in request.query_params.getlist(param_key):
            parameters.append(param_value)

    
    return parameters, marks_dict



# from pydantic import BaseModel
# class Job(BaseModel):
#     name: str
#     description: str
#     status: str = "pending"  # Default status is 'pending'

# jobs = []
# @app.post("/api/create")
# def create_job(job: Job):
#     jobs.append(job)
#     return {"jobs": jobs}

# @app.get("/api/jobs")
# def get_jobs():
#     return {"jobs": jobs}

# @app.delete("/api/jobs/{job_no}")
# def delete_job(job_no: int):
#     if 0 <= job_no < len(jobs):
#         deleted_job = jobs.pop(job_no)
#         return {"message": "Job deleted successfully", "job": deleted_job}
#     else:
#         return {"message": "Job not found"}, 404
    
