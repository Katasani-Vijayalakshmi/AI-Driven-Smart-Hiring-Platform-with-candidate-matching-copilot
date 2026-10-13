from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    candidate = "candidate"
    recruiter = "recruiter"

class ApplicationStatusEnum(str, enum.Enum):
    pending = "pending"
    under_review = "under_review"
    reviewed = "reviewed"
    shortlisted = "shortlisted"
    hold = "hold"
    accepted = "accepted"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)  # nullable: Google-only users have no password
    google_id = Column(String(128), unique=True, nullable=True, index=True)  # Google sub (provider ID)
    role = Column(Enum(RoleEnum), default=RoleEnum.candidate, nullable=False)

    # Extra Candidate Profile Fields
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    highest_degree = Column(String(100), nullable=True)
    university = Column(String(150), nullable=True)
    year_of_passing = Column(String(10), nullable=True)
    cgpa = Column(String(20), nullable=True)
    skills = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    applications = relationship("Application", back_populates="candidate", foreign_keys="[Application.user_id]")
    jobs = relationship("Job", back_populates="recruiter")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    department = Column(String(100), nullable=True)
    required_skills = Column(JSON, nullable=True) # Stored as list of strings
    experience_required = Column(Float, default=0.0)
    education_required = Column(String(100), nullable=True)
    
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recruiter = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    resume_file_path = Column(String(255), nullable=True)
    education = Column(String(255), nullable=True)
    university = Column(String(150), nullable=True)
    year_of_passing = Column(String(10), nullable=True)
    cgpa = Column(String(20), nullable=True)
    experience_years = Column(Float, default=0.0)
    skills = Column(JSON, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    
    status = Column(String(50), default="pending", nullable=False)
    hiring_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    candidate = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
