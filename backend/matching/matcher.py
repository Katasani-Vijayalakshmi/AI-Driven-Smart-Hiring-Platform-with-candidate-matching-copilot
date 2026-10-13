"""
backend/matching/matcher.py
============================
Core CandidateJobMatcher engine implementing 60/25/15 weighted compatibility scoring.
"""

from typing import Dict, Any, Tuple, List
from .skill_normalizer import match_skills, normalize_skill_list
from .skill_gap import generate_skill_gap_report
from .recommendation_engine import generate_skill_recommendations

class CandidateJobMatcher:
    """
    CandidateJobMatcher handles weighted evaluation:
      - Skill Score       -> 60%
      - Experience Score  -> 25%
      - Education Score   -> 15%
    """

    @staticmethod
    def calculate_skill_score(candidate_skills: List[str], required_skills: List[str]) -> Tuple[float, List[str], List[str], List[str]]:
        if not required_skills:
            return 1.0, candidate_skills, [], []
            
        matched, missing, partial = match_skills(candidate_skills, required_skills)
        ratio = len(matched) / len(required_skills)
        score = min(ratio, 1.0)
        return score, matched, missing, partial

    @staticmethod
    def calculate_experience_score(candidate_exp: float, required_exp: float) -> float:
        try:
            cand_e = float(candidate_exp or 0)
            req_e = float(required_exp or 0)
            if req_e <= 0:
                return 1.0
            return min(cand_e / req_e, 1.0)
        except Exception:
            return 0.5

    @staticmethod
    def calculate_education_score(candidate_edu: Any, required_edu: str) -> float:
        if not required_edu:
            return 1.0
            
        cand_edu_str = ""
        if isinstance(candidate_edu, list):
            cand_edu_str = " ".join(str(e) for e in candidate_edu).lower()
        elif isinstance(candidate_edu, str):
            cand_edu_str = candidate_edu.lower()
            
        req_edu_str = str(required_edu).lower()
        
        if req_edu_str in cand_edu_str or cand_edu_str in req_edu_str:
            return 1.0
            
        degrees = ["phd", "doctorate", "ms", "master", "m.tech", "mtech", "b.tech", "btech", "b.e", "be", "bachelor", "bs", "bsc", "degree"]
        if any(d in cand_edu_str for d in degrees):
            return 0.85
            
        return 0.5 if cand_edu_str else 0.0

    @classmethod
    def calculate_match(cls, candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main weighted matching formula:
          hiring_score = (skill_score * 0.60 + exp_score * 0.25 + edu_score * 0.15) * 100
        """
        cand_id = candidate.get("id") or candidate.get("candidate_id") or "cand_1"
        job_id = job.get("id") or job.get("job_id") or "job_1"
        cand_name = candidate.get("name") or candidate.get("username") or "Candidate"
        job_title = job.get("title") or "Position"

        cand_skills = candidate.get("skills") or []
        req_skills = job.get("required_skills") or []

        cand_exp = candidate.get("experience") or candidate.get("experience_years") or 0
        req_exp = job.get("experience_required") or job.get("experience") or 0

        cand_edu = candidate.get("education") or candidate.get("highest_degree") or ""
        req_edu = job.get("education_required") or job.get("education") or ""

        # 1. Skill Matching (60%)
        raw_skill_ratio, matched_skills, missing_skills, partial_skills = cls.calculate_skill_score(cand_skills, req_skills)
        skill_score = raw_skill_ratio * 100.0

        # 2. Experience Matching (25%)
        raw_exp_ratio = cls.calculate_experience_score(cand_exp, req_exp)
        exp_score = raw_exp_ratio * 100.0

        # 3. Education Matching (15%)
        raw_edu_ratio = cls.calculate_education_score(cand_edu, req_edu)
        edu_score = raw_edu_ratio * 100.0

        # Weighted hiring score (0-100)
        final_score = (raw_skill_ratio * 0.60 + raw_exp_ratio * 0.25 + raw_edu_ratio * 0.15) * 100.0
        hiring_score = round(final_score, 2)

        # Match Category
        if hiring_score >= 90.0:
            match_category = "Excellent Match"
            confidence = "High"
        elif hiring_score >= 75.0:
            match_category = "Strong Match"
            confidence = "High"
        elif hiring_score >= 60.0:
            match_category = "Moderate Match"
            confidence = "Medium"
        else:
            match_category = "Low Match"
            confidence = "Low"

        recommendations = generate_skill_recommendations(missing_skills)

        return {
            "candidate_id": cand_id,
            "job_id": job_id,
            "candidate": cand_name,
            "job_title": job_title,
            "hiring_score": hiring_score,
            "match_category": match_category,
            "confidence": confidence,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "partial_skills": partial_skills,
            "skill_score": round(skill_score, 2),
            "experience_score": round(exp_score, 2),
            "education_score": round(edu_score, 2),
            "recommendations": recommendations,
            "skill_gap_report": {
                "candidate": cand_name,
                "job_title": job_title,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "recommendations": recommendations
            }
        }

def calculate_match(candidate: Dict[str, Any], job: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Backward compatible helper function returning (hiring_score, matched_skills)."""
    res = CandidateJobMatcher.calculate_match(candidate, job)
    return res["hiring_score"], res["matched_skills"]
