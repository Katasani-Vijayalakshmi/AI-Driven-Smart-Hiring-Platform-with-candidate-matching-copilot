"""
backend/matching/skill_normalizer.py
======================================
Skill Normalization, Synonym Mapping & Semantic Matching Engine
"""

import json
import os
import re
from typing import List, Set, Dict, Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SYNONYMS_FILE = os.path.join(DATA_DIR, "skill_synonyms.json")

def load_synonyms() -> Dict[str, str]:
    if os.path.exists(SYNONYMS_FILE):
        try:
            with open(SYNONYMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "tf": "TensorFlow",
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "aws": "AWS",
        "k8s": "Kubernetes",
        "postgres": "PostgreSQL",
        "mongo": "MongoDB"
    }

SYNONYM_MAP = load_synonyms()

def normalize_skill(skill: str) -> str:
    """Clean string, strip punctuation, lower, apply synonym mapping."""
    if not skill or not isinstance(skill, str):
        return ""
    
    clean = skill.strip().lower()
    clean = re.sub(r'[^a-z0-9+#\s-]', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    
    if clean in SYNONYM_MAP:
        return SYNONYM_MAP[clean]
        
    return skill.strip()

def normalize_skill_list(skills: List[str]) -> List[str]:
    """Deduplicate and normalize a list of skill strings."""
    seen: Set[str] = set()
    result: List[str] = []
    for s in skills:
        norm = normalize_skill(s)
        if norm and norm.lower() not in seen:
            seen.add(norm.lower())
            result.append(norm)
    return result

def match_skills(candidate_skills: List[str], required_skills: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """
    Matches candidate skills against required job skills.
    Returns: (matched_skills, missing_skills, partial_skills)
    Supports semantic sub-string matching e.g. 'Deep Learning with TensorFlow' matching 'TensorFlow'.
    """
    cand_norm_map = {normalize_skill(s).lower(): s for s in candidate_skills if s}
    req_norm_map = {normalize_skill(r).lower(): r for r in required_skills if r}

    matched: List[str] = []
    missing: List[str] = []
    partial: List[str] = []

    for req_lower, req_orig in req_norm_map.items():
        if req_lower in cand_norm_map:
            matched.append(req_orig)
        else:
            # Semantic / Substring Match check
            is_partial = False
            for cand_lower, cand_orig in cand_norm_map.items():
                if (req_lower in cand_lower or cand_lower in req_lower) and len(req_lower) >= 2 and len(cand_lower) >= 2:
                    matched.append(req_orig)
                    partial.append(f"{req_orig} (~{cand_orig})")
                    is_partial = True
                    break
            if not is_partial:
                missing.append(req_orig)

    # Remove duplicates from matched keeping order
    seen = set()
    final_matched = []
    for m in matched:
        if m.lower() not in seen:
            seen.add(m.lower())
            final_matched.append(m)

    return final_matched, missing, partial
