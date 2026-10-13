"""
backend/nlp/skill_extractor.py
==============================
AI/NLP Automated Skill Extraction from Resume Text and Job Descriptions
"""

import json
import os
import re
from typing import List, Set, Dict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SKILLS_FILE = os.path.join(DATA_DIR, "skills.json")
SYNONYMS_FILE = os.path.join(DATA_DIR, "skill_synonyms.json")

def load_skill_db() -> Set[str]:
    all_skills = set()
    if os.path.exists(SKILLS_FILE):
        try:
            with open(SKILLS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cat, skill_list in data.items():
                    for s in skill_list:
                        all_skills.add(s)
        except Exception:
            pass
    if os.path.exists(SYNONYMS_FILE):
        try:
            with open(SYNONYMS_FILE, "r", encoding="utf-8") as f:
                syns = json.load(f)
                for val in syns.values():
                    all_skills.add(val)
        except Exception:
            pass
            
    default_skills = ["Python", "Java", "C++", "JavaScript", "TypeScript", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "AWS", "AWS SageMaker", "Kubernetes", "Docker", "FastAPI", "Pandas", "React"]
    all_skills.update(default_skills)
    return all_skills

SKILL_DB = load_skill_db()

def extract_skills_from_text(text: str) -> List[str]:
    if not text or not isinstance(text, str):
        return []
        
    extracted: Set[str] = set()
    clean_text = " " + text + " "
    
    for skill in SKILL_DB:
        pattern = r'(?i)(?<=[\s,.;:(])' + re.escape(skill) + r'(?=[\s,.;:)]|$)'
        if re.search(pattern, clean_text):
            extracted.add(skill)

    if re.search(r'(?i)ml', clean_text): extracted.add("Machine Learning")
    if re.search(r'(?i)dl', clean_text): extracted.add("Deep Learning")
    if re.search(r'(?i)tf', clean_text): extracted.add("TensorFlow")
    if re.search(r'(?i)k8s', clean_text): extracted.add("Kubernetes")
    if re.search(r'(?i)aws sagemaker', clean_text): extracted.add("AWS SageMaker")

    return list(extracted)
