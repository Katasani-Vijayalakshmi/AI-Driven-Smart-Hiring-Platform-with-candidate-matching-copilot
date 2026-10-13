"""
backend/matching/recommendation_engine.py
=========================================
Generates actionable learning recommendations based on missing skills.
"""

import json
import os
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REC_FILE = os.path.join(DATA_DIR, "recommendations.json")

def load_recommendations_map() -> Dict[str, str]:
    if os.path.exists(REC_FILE):
        try:
            with open(REC_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

REC_MAP = load_recommendations_map()

def generate_skill_recommendations(missing_skills: List[str]) -> List[str]:
    """Generates customized recommendations for missing skills."""
    if not missing_skills:
        return ["Excellent skill match! No major skill gaps detected."]
        
    recs = []
    for skill in missing_skills:
        clean_skill = skill.strip()
        if clean_skill in REC_MAP:
            recs.append(REC_MAP[clean_skill])
        else:
            # Check case-insensitive key
            matched_key = next((k for k in REC_MAP if k.lower() == clean_skill.lower()), None)
            if matched_key:
                recs.append(REC_MAP[matched_key])
            else:
                recs.append(f"Consider training in {clean_skill} to improve role compatibility.")
                
    return recs
