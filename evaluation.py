"""
evaluation.py
=============
Milestone 2 Metric Evaluation Script
Evaluates candidate-job matching accuracy against ground-truth benchmarks
and verifies 100% skill-gap report generation.
"""

import sys
sys.path.insert(0, ".")

from backend.matching.matcher import CandidateJobMatcher
from backend.services.matching_service import MatchingService
import pandas as pd

BENCHMARK_DATA = [
    {
        "candidate": {
            "name": "Sarah Johnson",
            "skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Data Analysis"],
            "experience": 5,
            "education": "MS Computer Science"
        },
        "job": {
            "title": "Senior Machine Learning Engineer",
            "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL"],
            "experience_required": 4,
            "education_required": "MS Computer Science"
        },
        "expected_score_range": (70.0, 95.0),
        "expected_category": "Strong Match"
    },
    {
        "candidate": {
            "name": "Alex Rivera",
            "skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL", "Docker", "Machine Learning"],
            "experience": 6,
            "education": "MS Computer Science"
        },
        "job": {
            "title": "Senior Machine Learning Engineer",
            "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL"],
            "experience_required": 4,
            "education_required": "MS Computer Science"
        },
        "expected_score_range": (90.0, 100.0),
        "expected_category": "Excellent Match"
    },
    {
        "candidate": {
            "name": "David Miller",
            "skills": ["HTML", "CSS", "Photoshop"],
            "experience": 1,
            "education": "BA Graphic Design"
        },
        "job": {
            "title": "Senior Machine Learning Engineer",
            "required_skills": ["Python", "TensorFlow", "Kubernetes", "AWS SageMaker", "SQL"],
            "experience_required": 4,
            "education_required": "MS Computer Science"
        },
        "expected_score_range": (0.0, 50.0),
        "expected_category": "Low Match"
    }
]

def run_evaluation():
    print("====================================================")
    print("MILESTONE 2: CANDIDATE-JOB MATCHING EVALUATION REPORT")
    print("====================================================\n")

    total_comparisons = 0
    skill_gap_reports_generated = 0
    accurate_matches = 0

    for idx, item in enumerate(BENCHMARK_DATA):
        total_comparisons += 1
        cand = item["candidate"]
        job = item["job"]
        
        match_result = CandidateJobMatcher.calculate_match(cand, job)
        
        if "skill_gap_report" in match_result and match_result["skill_gap_report"]:
            skill_gap_reports_generated += 1

        score = match_result["hiring_score"]
        category = match_result["match_category"]
        min_expected, max_expected = item["expected_score_range"]

        is_accurate = (min_expected <= score <= max_expected) and (category == item["expected_category"])
        if is_accurate:
            accurate_matches += 1

        print(f"Test Case {idx+1}: {cand['name']} -> {job['title']}")
        print(f"  Hiring Score: {score}% ({category})")
        print(f"  Matched Skills: {match_result['matched_skills']}")
        print(f"  Missing Skills: {match_result['missing_skills']}")
        print(f"  Recommendations: {match_result['recommendations']}")
        print(f"  Evaluation Status: {'ACCURATE' if is_accurate else 'MISMATCH'}\n")

    matching_accuracy = (accurate_matches / total_comparisons) * 100.0
    report_generation_rate = (skill_gap_reports_generated / total_comparisons) * 100.0

    print("====================================================")
    print("EVALUATION SUMMARY RESULTS:")
    print("====================================================")
    print(f"Total Benchmark Comparisons Evaluated : {total_comparisons}")
    print(f"Candidate-Job Matching Accuracy       : {matching_accuracy:.1f}% (Target >= 85%)")
    print(f"Skill-Gap Reports Generation Rate     : {report_generation_rate:.1f}% (Target = 100%)")
    print("====================================================")

    if matching_accuracy >= 85.0 and report_generation_rate == 100.0:
        print("\nMILESTONE 2 EVALUATION SUCCESSFUL! All target metrics achieved.")
    else:
        print("\nMetric targets not reached.")

if __name__ == "__main__":
    run_evaluation()
