from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    candidate = "candidate"
    recruiter = "recruiter"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.candidate

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    highest_degree: Optional[str] = None
    university: Optional[str] = None
    year_of_passing: Optional[str] = None
    cgpa: Optional[str] = None
    skills: Optional[List[str]] = []
    projects: Optional[List[Any]] = []
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class JobCreate(BaseModel):
    title: str
    department: Optional[str] = None
    required_skills: List[str] = []
    experience_required: float = 0.0
    education_required: Optional[str] = None

class JobResponse(JobCreate):
    id: int
    recruiter_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CandidateInfo(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    highest_degree: Optional[str] = None
    university: Optional[str] = None
    year_of_passing: Optional[str] = None
    cgpa: Optional[str] = None
    skills: Optional[List[str]] = []
    projects: Optional[List[Any]] = []
    
    class Config:
        from_attributes = True

class CandidateProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    highest_degree: Optional[str] = None
    university: Optional[str] = None
    year_of_passing: Optional[str] = None
    cgpa: Optional[str] = None
    skills: Optional[List[str]] = []
    projects: Optional[List[Any]] = []

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_file_path: Optional[str] = None
    education: Optional[str] = None
    university: Optional[str] = None
    year_of_passing: Optional[str] = None
    cgpa: Optional[str] = None
    experience_years: float = 0.0
    skills: Optional[List[str]] = []
    parsed_data: Optional[Any] = None
    status: str = "pending"
    hiring_score: float = 0.0
    created_at: Optional[datetime] = None
    candidate: Optional[CandidateInfo] = None
    
    class Config:
        from_attributes = True
