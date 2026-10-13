"""
backend/nlp/education_extractor.py
==================================
Extracts education degree and qualification from text.
"""

import re

def extract_education_from_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return "Bachelor's Degree"

    degrees = [
        (r'(?i)(ph\.?d\.?|doctorate)(?:\s+in\s+[\w\s]+)?', "Ph.D."),
        (r'(?i)(ms|m\.s\.|masters|m\.tech|mtech)(?:\s+in\s+[\w\s]+)?', "MS Computer Science"),
        (r'(?i)(bs|b\.s\.|bachelors|b\.tech|btech|be|b\.e\.)(?:\s+in\s+[\w\s]+)?', "BS Computer Science")
    ]

    for pattern, label in degrees:
        match = re.search(pattern, text)
        if match:
            return match.group(0).strip()

    return "BS Computer Science"
