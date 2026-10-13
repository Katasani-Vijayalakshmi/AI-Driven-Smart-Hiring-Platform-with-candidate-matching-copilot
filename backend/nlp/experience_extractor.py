"""
backend/nlp/experience_extractor.py
===================================
Extracts years of experience from unstructured text.
"""

import re

def extract_experience_from_text(text: str) -> float:
    if not text or not isinstance(text, str):
        return 0.0

    patterns = [
        r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?',
        r'(?:experience|exp)\s*(?:of)?\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)',
        r'(\d+(?:\.\d+)?)\s*\+\s*years?'
    ]

    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass

    return 0.0
