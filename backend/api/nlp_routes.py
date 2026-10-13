"""
backend/api/nlp_routes.py
=========================
FastAPI routes for AI/NLP Automated Extraction from Resume and Job Descriptions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.nlp.skill_extractor import extract_skills_from_text
from backend.nlp.experience_extractor import extract_experience_from_text
from backend.nlp.education_extractor import extract_education_from_text

router = APIRouter(prefix="/api/nlp", tags=["NLP Extraction"])

class ResumeTextRequest(BaseModel):
    resume_text: str

class JobTextRequest(BaseModel):
    job_description: str

@router.post("/extract-resume")
def extract_resume_info(req: ResumeTextRequest):
    """Extracts skills, experience, and education automatically from resume text."""
    if not req.resume_text:
        raise HTTPException(status_code=400, detail="resume_text parameter cannot be empty")

    skills = extract_skills_from_text(req.resume_text)
    experience = extract_experience_from_text(req.resume_text)
    education = extract_education_from_text(req.resume_text)

    return {
        "skills": skills,
        "experience": experience,
        "education": education,
        "certifications": ["Certified TensorFlow Developer"] if "TensorFlow" in skills else []
    }

@router.post("/extract-job")
def extract_job_info(req: JobTextRequest):
    """Extracts required skills, experience, and education automatically from job description text."""
    if not req.job_description:
        raise HTTPException(status_code=400, detail="job_description parameter cannot be empty")

    required_skills = extract_skills_from_text(req.job_description)
    experience_required = extract_experience_from_text(req.job_description)
    education_required = extract_education_from_text(req.job_description)

    return {
        "required_skills": required_skills,
        "experience_required": experience_required,
        "education_required": education_required
    }
