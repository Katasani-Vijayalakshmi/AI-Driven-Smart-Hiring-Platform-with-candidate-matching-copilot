"""
backend/matching/skill_gap.py
==============================
Generates Skill-Gap Analysis Reports for all evaluated candidates.
"""

from typing import Dict, Any, List
from .skill_normalizer import match_skills
from .recommendation_engine import generate_skill_recommendations

def generate_skill_gap_report(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a guaranteed skill gap report for candidate vs job.
    Includes matched_skills, missing_skills, recommendations.
    """
    cand_name = candidate.get("name") or candidate.get("username") or "Candidate"
    job_title = job.get("title") or "Position"
    
    cand_skills = candidate.get("skills") or []
    req_skills = job.get("required_skills") or []
    
    matched, missing, partial = match_skills(cand_skills, req_skills)
    recommendations = generate_skill_recommendations(missing)
    
    return {
        "candidate": cand_name,
        "job_title": job_title,
        "matched_skills": matched,
        "missing_skills": missing,
        "partial_skills": partial,
        "recommendations": recommendations,
        "summary": "Full skill match achieved." if not missing else f"Missing {len(missing)} required skills."
    }
