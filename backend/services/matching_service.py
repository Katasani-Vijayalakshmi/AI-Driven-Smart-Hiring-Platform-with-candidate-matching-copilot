"""
backend/services/matching_service.py
====================================
Service layer for candidate-job matching, ranking, and pandas DataFrame batch evaluation.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
from backend.matching.matcher import CandidateJobMatcher
from backend.nlp.skill_extractor import extract_skills_from_text
from backend.nlp.experience_extractor import extract_experience_from_text
from backend.nlp.education_extractor import extract_education_from_text

class MatchingService:

    @staticmethod
    def match_single(candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Matches a single candidate profile against a job description."""
        # Auto-extract skills if only text is provided
        if not candidate.get("skills") and candidate.get("resume_text"):
            candidate["skills"] = extract_skills_from_text(candidate["resume_text"])
            
        if not candidate.get("experience") and candidate.get("resume_text"):
            candidate["experience"] = extract_experience_from_text(candidate["resume_text"])

        if not job.get("required_skills") and job.get("description"):
            job["required_skills"] = extract_skills_from_text(job["description"])

        return CandidateJobMatcher.calculate_match(candidate, job)

    @staticmethod
    def rank_candidates_for_job(job: Dict[str, Any], candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ranks multiple candidates for a specific job in descending order of hiring score."""
        results = []
        for cand in candidates:
            match_res = MatchingService.match_single(cand, job)
            results.append(match_res)
            
        # Sort by hiring_score descending
        results.sort(key=lambda x: x["hiring_score"], reverse=True)
        
        # Add rank
        for idx, res in enumerate(results):
            res["rank"] = idx + 1
            
        return results

    @staticmethod
    def match_candidate_against_jobs(candidate: Dict[str, Any], jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Matches a single candidate against multiple jobs."""
        results = []
        for job in jobs:
            match_res = MatchingService.match_single(candidate, job)
            results.append(match_res)
            
        results.sort(key=lambda x: x["hiring_score"], reverse=True)
        return results

    @staticmethod
    def batch_match_dataframes(candidates_df: pd.DataFrame, jobs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs batch evaluation comparing every candidate in candidates_df against every job in jobs_df.
        Returns a ranked pandas DataFrame.
        """
        rows = []
        cands = candidates_df.to_dict(orient="records")
        jobs = jobs_df.to_dict(orient="records")

        for job in jobs:
            ranked_cands = MatchingService.rank_candidates_for_job(job, cands)
            for item in ranked_cands:
                rows.append({
                    "Rank": item["rank"],
                    "Candidate": item["candidate"],
                    "Job Title": item["job_title"],
                    "Hiring Score (%)": item["hiring_score"],
                    "Match Category": item["match_category"],
                    "Confidence": item["confidence"],
                    "Matched Skills": ", ".join(item["matched_skills"]),
                    "Missing Skills": ", ".join(item["missing_skills"]),
                    "Recommendations": "; ".join(item["recommendations"])
                })

        return pd.DataFrame(rows)
