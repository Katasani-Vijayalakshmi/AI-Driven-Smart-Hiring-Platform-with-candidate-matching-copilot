import pandas as pd
from backend.matching.matcher import CandidateJobMatcher
from backend.matching.skill_normalizer import normalize_skill, match_skills
from backend.matching.skill_gap import generate_skill_gap_report
from backend.nlp.skill_extractor import extract_skills_from_text
from backend.nlp.experience_extractor import extract_experience_from_text
from backend.nlp.education_extractor import extract_education_from_text
from backend.services.matching_service import MatchingService

def test_exact_skill_match():
    cand = {"name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"], "experience": 4, "education": "MS Computer Science"}
    job = {"title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "SQL"], "experience_required": 4, "education_required": "MS Computer Science"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["hiring_score"] == 100.0
    assert len(res["missing_skills"]) == 0

def test_partial_skill_match():
    cand = {"name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"], "experience": 4, "education": "MS Computer Science"}
    job = {"title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "SQL", "Kubernetes", "AWS SageMaker"], "experience_required": 4, "education_required": "MS Computer Science"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert 70.0 <= res["hiring_score"] <= 95.0
    assert "Kubernetes" in res["missing_skills"]

def test_no_skill_match():
    cand = {"name": "Bob", "skills": ["HTML", "CSS"], "experience": 1, "education": "BA English"}
    job = {"title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "SQL"], "experience_required": 5, "education_required": "MS Computer Science"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["hiring_score"] < 50.0
    assert res["match_category"] == "Low Match"

def test_experience_exceeds_requirement():
    cand = {"name": "Senior Dev", "skills": ["Python", "SQL"], "experience": 10, "education": "BS Computer Science"}
    job = {"title": "Dev", "required_skills": ["Python", "SQL"], "experience_required": 3, "education_required": "BS Computer Science"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["experience_score"] == 100.0

def test_experience_below_requirement():
    cand = {"name": "Junior Dev", "skills": ["Python", "SQL"], "experience": 1, "education": "BS Computer Science"}
    job = {"title": "Dev", "required_skills": ["Python", "SQL"], "experience_required": 4, "education_required": "BS Computer Science"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["experience_score"] == 25.0

def test_exact_education_match():
    cand = {"education": "MS Computer Science"}
    job = {"education_required": "MS Computer Science"}
    score = CandidateJobMatcher.calculate_education_score(cand["education"], job["education_required"])
    assert score == 1.0

def test_different_education():
    cand = {"education": "B.Tech Electrical"}
    job = {"education_required": "MS Computer Science"}
    score = CandidateJobMatcher.calculate_education_score(cand["education"], job["education_required"])
    assert 0.5 <= score <= 0.85

def test_skill_synonyms():
    norm1 = normalize_skill("ML")
    norm2 = normalize_skill("k8s")
    assert norm1.lower() == "machine learning"
    assert norm2.lower() == "kubernetes"

def test_empty_candidate_skills():
    cand = {"name": "No Skills", "skills": [], "experience": 2, "education": "BS"}
    job = {"title": "Dev", "required_skills": ["Python", "SQL"], "experience_required": 2, "education_required": "BS"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["skill_score"] == 0.0

def test_empty_job_skills():
    cand = {"name": "Dev", "skills": ["Python"], "experience": 2, "education": "BS"}
    job = {"title": "Dev", "required_skills": [], "experience_required": 2, "education_required": "BS"}
    res = CandidateJobMatcher.calculate_match(cand, job)
    assert res["skill_score"] == 100.0

def test_multiple_candidate_matching():
    job = {"title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "SQL"], "experience_required": 3}
    cands = [
        {"id": 1, "name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"], "experience": 5},
        {"id": 2, "name": "John", "skills": ["Python"], "experience": 1}
    ]
    ranked = MatchingService.rank_candidates_for_job(job, cands)
    assert ranked[0]["candidate"] == "Sarah"
    assert ranked[0]["rank"] == 1

def test_multiple_job_matching():
    cand = {"name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"], "experience": 5}
    jobs = [
        {"id": 1, "title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "SQL"], "experience_required": 4},
        {"id": 2, "title": "Frontend Engineer", "required_skills": ["React", "CSS", "HTML"], "experience_required": 2}
    ]
    results = MatchingService.match_candidate_against_jobs(cand, jobs)
    assert results[0]["job_title"] == "ML Engineer"

def test_nlp_extraction():
    resume_text = "Sarah Johnson is a Machine Learning Engineer with 5 years of experience in Python, TensorFlow, SQL and Machine Learning. She completed an MS in Computer Science."
    skills = extract_skills_from_text(resume_text)
    exp = extract_experience_from_text(resume_text)

    assert "Python" in skills
    assert "TensorFlow" in skills
    assert exp == 5.0

def test_skill_gap_generation():
    cand = {"name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"]}
    job = {"title": "ML Engineer", "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL"]}
    report = generate_skill_gap_report(cand, job)

    assert report["candidate"] == "Sarah"
    assert "Kubernetes" in report["missing_skills"]
    assert len(report["recommendations"]) > 0

def test_batch_dataframe_matching():
    cands_df = pd.DataFrame([
        {"id": 1, "name": "Sarah", "skills": ["Python", "TensorFlow", "SQL"], "experience": 5, "education": "MS"},
        {"id": 2, "name": "John", "skills": ["Python", "SQL"], "experience": 2, "education": "BS"}
    ])
    jobs_df = pd.DataFrame([
        {"id": 101, "title": "Senior ML Engineer", "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL"], "experience_required": 4, "education_required": "MS"}
    ])
    df_res = MatchingService.batch_match_dataframes(cands_df, jobs_df)
    assert len(df_res) == 2
    assert "Hiring Score (%)" in df_res.columns
