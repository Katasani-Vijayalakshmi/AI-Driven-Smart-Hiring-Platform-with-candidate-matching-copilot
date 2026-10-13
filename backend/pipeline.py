"""
backend/pipeline.py
===================
End-to-End Orchestration — Part 1 & 2
Combines resume loading, profiling, job analysis, and matching.
"""

import os
from backend.resume_loader import load_resume
from backend.candidate_extractor import extract_candidate_info
from backend.job_analyzer import analyze_job_description
from backend.matching_engine import calculate_match
from backend.skill_gap import skill_gap_analysis
from backend.ranking import rank_candidates
# Optional: from backend.nlp_extractor import extract_skills_nlp

def process_candidate_resume(file_path: str) -> dict:
    """End-to-end pipeline for processing a single resume file."""
    print(f"Loading resume: {file_path}")
    text = load_resume(file_path)
    print("Extracting candidate info...")
    candidate = extract_candidate_info(text)
    candidate["source_file"] = os.path.basename(file_path)
    
    # Example of incorporating NLP extractor (uncomment if transformers installed)
    # nlp_skills = extract_skills_nlp(text)
    # candidate["skills"] = list(set(candidate["skills"] + nlp_skills))
    
    return candidate

def process_job_description(file_path: str) -> dict:
    """End-to-end pipeline for processing a job description file."""
    print(f"Loading JD: {file_path}")
    text = load_resume(file_path)  # re-use loader for simplicity
    print("Analyzing JD...")
    job_reqs = analyze_job_description(text)
    return job_reqs

def run_matching_pipeline(resume_paths: list, jd_path: str):
    """
    Process multiple resumes against a job description,
    calculate matches, and return a ranked DataFrame.
    """
    job = process_job_description(jd_path)
    
    candidates = []
    for path in resume_paths:
        try:
            cand = process_candidate_resume(path)
            candidates.append(cand)
        except Exception as e:
            print(f"Error processing {path}: {e}")
            
    print("\nRanking Candidates...")
    df = rank_candidates(candidates, job)
    return df

if __name__ == "__main__":
    print("Pipeline ready.")
    # Example usage:
    # df = run_matching_pipeline(["resume1.pdf", "resume2.docx"], "job_desc.pdf")
    # print(df)
