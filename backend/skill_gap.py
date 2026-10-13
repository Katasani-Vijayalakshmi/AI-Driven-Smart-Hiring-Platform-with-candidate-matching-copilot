"""
backend/skill_gap.py
====================
Skill Gap Analysis — Part 2, Milestone 2
Identifies missing skills and generates recommendations.
"""

from typing import Dict, Any

def skill_gap_analysis(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare candidate skills against job requirements to identify gaps.
    
    Args:
        candidate: Candidate dictionary.
        job: Job dictionary.
        
    Returns:
        Dictionary containing gap analysis report.
    """
    required_skills = set(job.get("required_skills", []))
    candidate_skills = set(candidate.get("skills", []))
    
    matched_skills = required_skills.intersection(candidate_skills)
    missing_skills = required_skills - candidate_skills
    
    recommendations = []
    for skill in missing_skills:
        recommendations.append(f"Consider training or certification in {skill}")
        
    # Also check experience gap
    job_exp = job.get("experience_required", 0)
    cand_exp = candidate.get("experience_years", 0)
    exp_gap = max(0, job_exp - cand_exp)
    
    if exp_gap > 0:
        recommendations.append(f"Requires {exp_gap} more years of experience.")
        
    report = {
        "candidate": candidate.get("name", "Unknown Candidate"),
        "job_title": job.get("title", "Unknown Job"),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "recommendations": recommendations,
        "experience_gap_years": exp_gap
    }
    
    return report

if __name__ == "__main__":
    cand = {
        "name": "Sarah Johnson",
        "skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Data Analysis"],
        "experience_years": 3.0,
    }
    
    job_req = {
        "title": "Senior Machine Learning Engineer",
        "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS", "SQL"],
        "experience_required": 4.0,
    }
    
    report = skill_gap_analysis(cand, job_req)
    import json
    print(json.dumps(report, indent=2))
