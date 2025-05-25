from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try loading the JSON file safely
marks_dict = {}
try:
    with open("q-vercel-python.json", "r") as file:
        data = json.load(file)
        marks_dict = {entry["name"]: entry["marks"] for entry in data}
except Exception as e:
    print("ERROR loading JSON:", e)
    marks_dict = {}

@app.get("/")
def index():
    return {"message": "API is live"}

@app.get("/api")
def get_marks(name: list[str] = []):
    print("Received query:", name)
    result = [marks_dict.get(n, None) for n in name]
    print("Resulting marks:", result)
    return {"marks": result}
