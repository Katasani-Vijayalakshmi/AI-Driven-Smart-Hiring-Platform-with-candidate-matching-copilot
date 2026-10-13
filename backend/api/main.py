from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta
from pydantic import BaseModel
import os
import shutil
import asyncio

from . import models, schemas, auth, database, matching_routes, nlp_routes, google_auth
from backend.pipeline import process_candidate_resume
from backend.matching_engine import calculate_match, calculate_detailed_match
from backend.interview_generator import (
    get_role_questions, 
    evaluate_mock_interview, 
    evaluate_voice_screening_session
)

class StatusUpdate(BaseModel):
    status: str

class MockInterviewSubmission(BaseModel):
    role: str = "Machine Learning Engineer"
    responses: List[Dict[str, Any]] = []

class VoiceScreeningSubmission(BaseModel):
    questions_answered: int = 5
    duration_seconds: int = 300

# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Recruitment Copilot API")

app.include_router(matching_routes.router)
app.include_router(nlp_routes.router)
app.include_router(google_auth.router)  # Google OAuth routes (/api/auth/google, /api/auth/google/callback)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Authentication Routes ──

@app.post("/api/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        (models.User.username == form_data.username) | (models.User.email == form_data.username)
    ).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value}

@app.get("/api/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# ── Job Management Routes ──

@app.post("/api/jobs", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_recruiter)):
    db_job = models.Job(**job.model_dump(), recruiter_id=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/api/jobs", response_model=List[schemas.JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Job).offset(skip).limit(limit).all()

@app.get("/api/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(database.get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job


# ── Recruiter Portal Routes ──

@app.get("/api/applications", response_model=List[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_recruiter)):
    return db.query(models.Application).options(joinedload(models.Application.candidate), joinedload(models.Application.job)).all()

@app.patch("/api/applications/{app_id}/status")
def update_application_status(
    app_id: int, 
    update: StatusUpdate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_active_recruiter)
):
    valid_statuses = ["pending", "under_review", "reviewed", "shortlisted", "hold", "accepted", "rejected"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = update.status
    db.commit()
    db.refresh(app)
    return {"id": app.id, "status": app.status, "message": f"Application status updated to {app.status}"}

@app.get("/api/recruiter/job-stats")
def get_recruiter_job_stats(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_recruiter)
):
    jobs = db.query(models.Job).all()
    stats = []
    for j in jobs:
        apps = db.query(models.Application).filter(models.Application.job_id == j.id).all()
        status_counts = {
            "under_review": sum(1 for a in apps if a.status in ["pending", "under_review"]),
            "reviewed": sum(1 for a in apps if a.status == "reviewed"),
            "shortlisted": sum(1 for a in apps if a.status == "shortlisted"),
            "hold": sum(1 for a in apps if a.status == "hold"),
            "accepted": sum(1 for a in apps if a.status == "accepted"),
            "rejected": sum(1 for a in apps if a.status == "rejected"),
        }
        avg_score = round(sum(a.hiring_score for a in apps) / len(apps), 1) if apps else 0.0
        stats.append({
            "job_id": j.id,
            "title": j.title,
            "department": j.department,
            "total_applicants": len(apps),
            "avg_match_score": avg_score,
            "status_counts": status_counts
        })
    return stats

@app.get("/api/recruiter/analytics")
def get_recruiter_analytics(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_active_recruiter)
):
    total_apps = db.query(models.Application).count()
    total_jobs = db.query(models.Job).count()
    total_candidates = db.query(models.User).filter(models.User.role == models.RoleEnum.candidate).count()
    
    apps = db.query(models.Application).all()
    status_summary = {
        "reviewed": sum(1 for a in apps if a.status == "reviewed"),
        "under_review": sum(1 for a in apps if a.status in ["pending", "under_review"]),
        "hold": sum(1 for a in apps if a.status == "hold"),
        "shortlisted": sum(1 for a in apps if a.status == "shortlisted"),
        "accepted": sum(1 for a in apps if a.status == "accepted"),
        "rejected": sum(1 for a in apps if a.status == "rejected")
    }
    
    return {
        "total_jobs": total_jobs,
        "total_candidates": total_candidates,
        "total_applications": total_apps,
        "status_summary": status_summary
    }


# ── Candidate Portal Routes ──

@app.post("/api/candidate/parse-resume")
async def parse_candidate_resume(
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resume files are supported.")
    
    file_location = f"{UPLOAD_DIR}/{current_user.username}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    try:
        parsed = await asyncio.to_thread(process_candidate_resume, file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")
        
    # Auto-update candidate profile fields if not already populated
    if parsed.get("name") and not current_user.full_name:
        current_user.full_name = parsed["name"]
    if parsed.get("phone") and not current_user.phone:
        current_user.phone = parsed["phone"]
    if parsed.get("location") and not current_user.location:
        current_user.location = parsed["location"]
    if parsed.get("highest_degree") and not current_user.highest_degree:
        current_user.highest_degree = parsed["highest_degree"]
    if parsed.get("university") and not current_user.university:
        current_user.university = parsed["university"]
    if parsed.get("year_of_passing") and not current_user.year_of_passing:
        current_user.year_of_passing = parsed["year_of_passing"]
    if parsed.get("cgpa") and not current_user.cgpa:
        current_user.cgpa = parsed["cgpa"]
    if parsed.get("skills"):
        current_user.skills = list(set((current_user.skills or []) + parsed["skills"]))
    if parsed.get("projects") and not current_user.projects:
        current_user.projects = parsed["projects"]
        
    db.commit()
    db.refresh(current_user)
    
    return {
        "filename": file.filename,
        "parsed_data": parsed,
        "user": current_user
    }

@app.post("/api/apply/{job_id}", response_model=schemas.ApplicationResponse)
async def apply_for_job(
    job_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != models.RoleEnum.candidate:
        raise HTTPException(status_code=403, detail="Only candidates can apply")
        
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Save file
    file_location = f"{UPLOAD_DIR}/{current_user.username}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    # Process Resume with AI Engine non-blockingly
    try:
        parsed_profile = await asyncio.to_thread(process_candidate_resume, file_location)
        
        job_dict = {
            "title": job.title,
            "required_skills": job.required_skills,
            "experience_required": job.experience_required,
            "education_required": job.education_required
        }
        
        detailed = calculate_detailed_match(parsed_profile, job_dict)
        hiring_score = detailed["overall_score"]
        
    except Exception as e:
        print(f"Error parsing resume: {e}")
        parsed_profile = {}
        hiring_score = 0.0

    # Auto-update user profile with extracted data
    if parsed_profile.get("name") and not current_user.full_name:
        current_user.full_name = parsed_profile["name"]
    if parsed_profile.get("phone") and not current_user.phone:
        current_user.phone = parsed_profile["phone"]
    if parsed_profile.get("highest_degree") and not current_user.highest_degree:
        current_user.highest_degree = parsed_profile["highest_degree"]
    if parsed_profile.get("university") and not current_user.university:
        current_user.university = parsed_profile["university"]
    if parsed_profile.get("year_of_passing") and not current_user.year_of_passing:
        current_user.year_of_passing = parsed_profile["year_of_passing"]
    if parsed_profile.get("cgpa") and not current_user.cgpa:
        current_user.cgpa = parsed_profile["cgpa"]
    if parsed_profile.get("skills"):
        current_user.skills = list(set((current_user.skills or []) + parsed_profile["skills"]))
    if parsed_profile.get("projects") and not current_user.projects:
        current_user.projects = parsed_profile["projects"]

    # Create application
    db_app = models.Application(
        user_id=current_user.id,
        job_id=job_id,
        resume_file_path=file_location,
        education=", ".join(parsed_profile.get("education", [])) or parsed_profile.get("highest_degree"),
        university=parsed_profile.get("university"),
        year_of_passing=parsed_profile.get("year_of_passing"),
        cgpa=parsed_profile.get("cgpa"),
        experience_years=parsed_profile.get("experience_years", 0),
        skills=parsed_profile.get("skills", []),
        parsed_data=parsed_profile,
        hiring_score=hiring_score
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@app.get("/api/my-applications", response_model=List[schemas.ApplicationResponse])
def get_my_applications(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Application).filter(models.Application.user_id == current_user.id).options(joinedload(models.Application.job)).all()

@app.post("/api/candidate/profile", response_model=schemas.UserResponse)
def update_candidate_profile(
    profile: schemas.CandidateProfileUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if profile.full_name: current_user.full_name = profile.full_name
    if profile.phone: current_user.phone = profile.phone
    if profile.location: current_user.location = profile.location
    if profile.address: current_user.address = profile.address
    if profile.highest_degree: current_user.highest_degree = profile.highest_degree
    if profile.university: current_user.university = profile.university
    if profile.year_of_passing: current_user.year_of_passing = profile.year_of_passing
    if profile.cgpa: current_user.cgpa = profile.cgpa
    if profile.skills: current_user.skills = profile.skills
    if profile.projects: current_user.projects = profile.projects
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/api/candidate/match-job/{job_id}")
@app.post("/api/candidate/match-job/{job_id}")
def match_candidate_to_job(
    job_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    cand_dict = {
        "name": current_user.full_name or current_user.username,
        "skills": current_user.skills or [],
        "experience_years": getattr(current_user, 'experience_years', 0) or 0,
        "highest_degree": current_user.highest_degree,
        "university": current_user.university,
        "projects": current_user.projects or []
    }
    
    job_dict = {
        "title": job.title,
        "required_skills": job.required_skills or [],
        "experience_required": job.experience_required or 0,
        "education_required": job.education_required
    }
    
    analysis = calculate_detailed_match(cand_dict, job_dict)
    return analysis


# ── Interview Prep & AI Simulation Routes ──

@app.get("/api/interview-questions")
def get_interview_questions_api(
    role: Optional[str] = "Machine Learning Engineer",
    category: Optional[str] = None,
    count: int = Query(15, ge=5, le=30),
    job_id: Optional[int] = None,
    db: Session = Depends(database.get_db),
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    cand_profile = None
    missing_skills = None
    
    if current_user:
        cand_profile = {
            "skills": current_user.skills or [],
            "experience_years": getattr(current_user, 'experience_years', 0) or 0,
            "highest_degree": current_user.highest_degree
        }
        
    if job_id:
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if job and cand_profile:
            job_dict = {"title": job.title, "required_skills": job.required_skills or []}
            match_res = calculate_detailed_match(cand_profile, job_dict)
            missing_skills = match_res.get("missing_skills", [])
            
    questions = get_role_questions(
        role=role,
        category=category,
        count=count,
        candidate_profile=cand_profile,
        missing_skills=missing_skills
    )
    return questions

@app.post("/api/interview/evaluate")
def evaluate_interview_api(submission: MockInterviewSubmission):
    eval_result = evaluate_mock_interview(submission.responses, role=submission.role)
    return eval_result

@app.post("/api/voice-screening/evaluate")
def evaluate_voice_screening_api(submission: VoiceScreeningSubmission):
    report = evaluate_voice_screening_session({
        "questions_answered": submission.questions_answered,
        "duration_seconds": submission.duration_seconds
    })
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.main:app", host="127.0.0.1", port=8000, reload=True)
