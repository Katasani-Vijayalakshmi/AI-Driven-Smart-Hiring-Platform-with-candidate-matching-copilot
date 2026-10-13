"""
backend/job_analyzer.py
========================
Job Description Analysis — Part 1, Milestone 1
Extracts structured requirements from raw job description text.
"""

import re
from typing import Dict, Any, List

# Re-use the same common skills list for basic extraction
from backend.candidate_extractor import COMMON_SKILLS

def analyze_job_description(text: str) -> Dict[str, Any]:
    """
    Extract structured requirements from a job description text.

    Args:
        text: Raw JD text.

    Returns:
        Dictionary containing extracted job requirements.
    """
    job_reqs = {
        "title": "Extracted Job Title", # Placeholder, usually provided separately
        "required_skills": [],
        "experience_required": 0.0,
        "education_required": None
    }

    if not text:
        return job_reqs
    
    text_lower = text.lower()

    # 1. Extract Skills (Keyword Matching)
    extracted_skills = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            extracted_skills.append(skill)
    
    job_reqs["required_skills"] = extracted_skills

    # 2. Extract Experience Required (Simple Heuristic)
    # Looking for patterns like "5+ years", "3-5 years", "minimum 4 years"
    exp_matches = re.findall(r'(\d+)(?:\s*(?:-|to|\+)?\s*\d*)?\s*(?:\+|plus)?\s*years?', text_lower)
    if exp_matches:
        # Take the maximum number mentioned near "years" as a rough estimate
        try:
            years = [float(y) for y in exp_matches]
            job_reqs["experience_required"] = max(years)
        except ValueError:
            pass

    # 3. Extract Education Required
    if any(kw in text_lower for kw in ["phd", "ph.d", "doctorate"]):
        job_reqs["education_required"] = "PhD"
    elif any(kw in text_lower for kw in ["master", "ms ", "m.s.", "m.a.", "mba"]):
        job_reqs["education_required"] = "Master's Degree"
    elif any(kw in text_lower for kw in ["bachelor", "bs ", "b.s.", "b.a.", "degree"]):
        job_reqs["education_required"] = "Bachelor's Degree"
    
    return job_reqs

if __name__ == "__main__":
    sample_jd = """
    Senior Machine Learning Engineer
    
    Requirements:
    - Minimum 5 years of experience in software engineering.
    - Strong proficiency in Python and SQL.
    - Experience with Machine Learning frameworks like TensorFlow or PyTorch.
    - Master's degree in Computer Science or related field.
    - Experience with Docker and Kubernetes is a plus.
    """
    
    print("Testing JD analyzer:")
    reqs = analyze_job_description(sample_jd)
    import json
    print(json.dumps(reqs, indent=2))
