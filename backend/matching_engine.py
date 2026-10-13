"""
backend/matching_engine.py
==========================
Candidate Matching & Skill Analysis Engine
Calculates compatibility score between candidate profile/resume and job description.
Uses weighted multi-factor evaluation:
  - Required Skills Match   → 50%
  - Preferred Skills Match  → 20%
  - Experience Relevance    → 15%
  - Education Relevance     → 10%
  - Project Relevance       → 5%
"""

from typing import Dict, Any, Tuple, List, Set

def normalize_skill(s: str) -> str:
    return s.strip().lower().replace(".", "").replace("-", " ")

def calculate_detailed_match(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detailed multi-dimensional job matching and skill gap analysis.
    """
    cand_skills_raw = candidate.get("skills", []) or []
    req_skills_raw = job.get("required_skills", []) or []
    
    cand_skills_norm = {normalize_skill(s): s for s in cand_skills_raw}
    req_skills_norm = {normalize_skill(s): s for s in req_skills_raw}
    
    # 1. Exact Matching Skills
    matched_skills = []
    missing_skills = []
    partial_skills = []
    
    for norm_req, orig_req in req_skills_norm.items():
        if norm_req in cand_skills_norm:
            matched_skills.append(orig_req)
        else:
            # Check for partial / related matches (e.g. "REST API" ~ "FastAPI", "ML" ~ "Machine Learning")
            is_partial = False
            for norm_cand, orig_cand in cand_skills_norm.items():
                if (norm_req in norm_cand or norm_cand in norm_req) and len(norm_req) > 2 and len(norm_cand) > 2:
                    partial_skills.append(f"{orig_req} (~{orig_cand})")
                    is_partial = True
                    break
            if not is_partial:
                missing_skills.append(orig_req)

    # Required Skills Score (50%)
    if req_skills_raw:
        req_ratio = (len(matched_skills) + 0.5 * len(partial_skills)) / len(req_skills_raw)
        req_score = min(req_ratio, 1.0) * 50.0
    else:
        req_score = 50.0

    # Preferred / Extra Candidate Skills Score (20%)
    extra_skills = [s for norm_s, s in cand_skills_norm.items() if norm_s not in req_skills_norm]
    pref_score = min(len(extra_skills) / 4.0, 1.0) * 20.0

    # Experience Score (15%)
    job_exp = float(job.get("experience_required", 0) or 0)
    cand_exp = float(candidate.get("experience_years", 0) or 0)
    if job_exp > 0:
        exp_score = min(cand_exp / job_exp, 1.0) * 15.0
    else:
        exp_score = 15.0

    # Education Score (10%)
    job_edu = (job.get("education_required") or "").lower()
    cand_edu = [str(e).lower() for e in (candidate.get("education", []) or [])]
    if candidate.get("highest_degree"):
        cand_edu.append(str(candidate["highest_degree"]).lower())
        
    edu_score = 10.0
    if job_edu:
        if any(deg in " ".join(cand_edu) for deg in ["b.tech", "btech", "b.e", "be", "bachelor", "bs", "bsc", "master", "m.tech", "ms", "phd", "degree"]):
            edu_score = 10.0
        elif cand_edu:
            edu_score = 7.5
        else:
            edu_score = 5.0

    # Project Relevance Score (5%)
    cand_projects = candidate.get("projects", []) or []
    proj_score = 5.0 if cand_projects else 2.5
    if cand_projects:
        # Check if project technologies match required skills
        proj_tech_matches = 0
        for p in cand_projects:
            p_tech = [normalize_skill(t) for t in (p.get("tech", []) or [])]
            if any(t in req_skills_norm for t in p_tech):
                proj_tech_matches += 1
        if proj_tech_matches > 0:
            proj_score = 5.0
        else:
            proj_score = 4.0

    overall_score = round(req_score + pref_score + exp_score + edu_score + proj_score, 1)
    overall_score = min(max(overall_score, 10.0), 100.0)

    # Generate Explanation Text
    matched_str = ", ".join(matched_skills[:4]) if matched_skills else "none"
    missing_str = ", ".join(missing_skills[:3]) if missing_skills else "none"
    
    if len(matched_skills) >= len(req_skills_raw) * 0.7:
        explanation = f"Your profile is a strong match! You cover key requirements including {matched_str}. " + (f"Consider learning {missing_str} to reach 100%." if missing_skills else "You meet all primary criteria!")
    elif len(matched_skills) > 0:
        explanation = f"Your profile matches with {matched_str}. However, {missing_str} {'is' if len(missing_skills)==1 else 'are'} currently missing from your resume."
    else:
        explanation = f"Your technical profile has significant gaps for this role. Missing core skills: {missing_str}."

    recommendations = []
    for ms in missing_skills[:4]:
        recommendations.append(f"Complete a project or certification demonstrating hands-on experience with {ms}.")
    if cand_exp < job_exp:
        recommendations.append(f"Highlight academic or freelance project experience to compensate for the {job_exp} year experience requirement.")

    return {
        "job_title": job.get("title", "Position"),
        "overall_score": overall_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "partial_skills": partial_skills,
        "candidate_skills": cand_skills_raw,
        "required_skills": req_skills_raw,
        "breakdown": {
            "required_skills": round(req_score, 1),
            "preferred_skills": round(pref_score, 1),
            "experience_relevance": round(exp_score, 1),
            "education_relevance": round(edu_score, 1),
            "project_relevance": round(proj_score, 1)
        },
        "explanation": explanation,
        "recommendations": recommendations
    }

def calculate_match(candidate: Dict[str, Any], job: Dict[str, Any]) -> Tuple[float, list]:
    """Backward-compatible tuple return for existing pipeline calls."""
    res = calculate_detailed_match(candidate, job)
    return res["overall_score"], res["matched_skills"]

if __name__ == "__main__":
    cand = {
        "name": "Sarah Johnson",
        "skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Data Analysis"],
        "experience_years": 5.0,
        "education": ["MS Computer Science"]
    }
    
    job_req = {
        "title": "Senior Machine Learning Engineer",
        "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS", "SQL"],
        "experience_required": 4.0,
        "education_required": "Master's Degree"
    }
    
    score, matched = calculate_match(cand, job_req)
    print(f"Hiring Score: {score}%")
    print(f"Matched Skills: {matched}")
