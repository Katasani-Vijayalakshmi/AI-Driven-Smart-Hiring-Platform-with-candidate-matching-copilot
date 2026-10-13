"""
backend/ranking.py
==================
Candidate Ranking — Part 2, Milestone 2
Scores and ranks multiple candidates for a job using DataFrames.
"""

import pandas as pd
from typing import List, Dict, Any
from backend.matching_engine import calculate_match
from backend.skill_gap import skill_gap_analysis

def rank_candidates(candidates: List[Dict[str, Any]], job: Dict[str, Any]) -> pd.DataFrame:
    """
    Score and rank a list of candidates against a job description.
    
    Args:
        candidates: List of candidate dictionaries.
        job: Job dictionary.
        
    Returns:
        pandas DataFrame sorted by hiring_score in descending order.
    """
    rows = []
    
    for c in candidates:
        score, matched = calculate_match(c, job)
        gap = skill_gap_analysis(c, job)
        
        rows.append({
            "name": c.get("name", "Unknown"),
            "email": c.get("email", ""),
            "experience_years": c.get("experience_years", 0),
            "hiring_score": score,
            "matched_skills": ", ".join(matched),
            "missing_skills": ", ".join(gap["missing_skills"]),
            "recommendations": " | ".join(gap["recommendations"])
        })
        
    df = pd.DataFrame(rows)
    
    if not df.empty:
        df = df.sort_values(by="hiring_score", ascending=False).reset_index(drop=True)
        
    return df

if __name__ == "__main__":
    candidates_list = [
        {"name": "Alice", "skills": ["Python", "SQL", "AWS"], "experience_years": 3},
        {"name": "Bob", "skills": ["Java", "SQL"], "experience_years": 5},
        {"name": "Charlie", "skills": ["Python", "TensorFlow", "AWS", "SQL"], "experience_years": 4}
    ]
    
    job_req = {
        "title": "Data Engineer",
        "required_skills": ["Python", "AWS", "SQL", "Spark"],
        "experience_required": 3
    }
    
    df = rank_candidates(candidates_list, job_req)
    print("Ranked Candidates:")
    print(df.to_string())
