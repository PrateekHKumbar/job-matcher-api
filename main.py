import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import database
import matcher

app = FastAPI(
    title="Job Application Tracker & Resume Matcher API",
    description="A production-ready REST API for intelligent ATS resume matching and job application tracking.",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
database.init_db()

# --- Pydantic Data Models ---
class MatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Raw text of the resume")
    job_description: str = Field(..., min_length=10, description="Raw text of the job description")

class JobCreate(BaseModel):
    company: str
    role: str
    location: str = "Remote"
    status: str = "Applied"
    match_score: float = 0.0
    job_description: str = ""
    notes: str = ""

class JobUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

# --- API Endpoints ---

@app.post("/api/match", summary="Analyze resume match against job description")
def match_resume(payload: MatchRequest):
    """
    Computes TF-IDF vectorization, Cosine Similarity score,
    and extracts matched vs missing technical keywords.
    """
    results = matcher.analyze_match(payload.resume_text, payload.job_description)
    return results

@app.get("/api/jobs", summary="Get all tracked job applications")
def list_jobs(status: Optional[str] = Query(None, description="Filter by status (Applied, Screening, Interview, Offered, Rejected)")):
    """Retrieve all tracked applications with optional status filter."""
    return database.get_all_jobs(status_filter=status)

@app.post("/api/jobs", summary="Create a new job application entry", status_code=201)
def add_job(job: JobCreate):
    """Save an applied job with company, role, match score, and notes."""
    created = database.create_job(
        company=job.company,
        role=job.role,
        location=job.location,
        status=job.status,
        match_score=job.match_score,
        job_description=job.job_description,
        notes=job.notes
    )
    return created

@app.get("/api/jobs/{job_id}", summary="Get job application by ID")
def get_job(job_id: int):
    job = database.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job application not found")
    return job

@app.put("/api/jobs/{job_id}", summary="Update application status or notes")
def update_job(job_id: int, payload: JobUpdate):
    updated = database.update_job_status(job_id, payload.status, payload.notes)
    if not updated:
        raise HTTPException(status_code=404, detail="Job application not found")
    return updated

@app.delete("/api/jobs/{job_id}", summary="Delete an application")
def remove_job(job_id: int):
    success = database.delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job application not found")
    return {"message": "Job application deleted successfully"}

@app.get("/api/stats", summary="Get high-level application metrics")
def get_metrics():
    """Returns total applications, status distribution, and average match score."""
    return database.get_stats()

# Mount static frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_dashboard():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Job Tracker API is running. Visit /docs for Swagger API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
