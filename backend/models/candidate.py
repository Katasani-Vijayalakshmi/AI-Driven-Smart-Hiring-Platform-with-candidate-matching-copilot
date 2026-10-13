"""
backend/models/candidate.py
============================
Candidate dataclass and pandas DataFrame schema.
Part of: AI Recruitment Copilot — Part 1
"""

from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd


# ── Candidate Dataclass ────────────────────────────────────────
@dataclass
class Candidate:
    """Structured candidate profile extracted from a resume."""

    name:             Optional[str]       = None
    email:            Optional[str]       = None
    phone:            Optional[str]       = None
    location:         Optional[str]       = None
    experience_years: float               = 0.0
    education:        List[str]           = field(default_factory=list)
    skills:           List[str]           = field(default_factory=list)
    certifications:   List[str]           = field(default_factory=list)
    projects:         List[str]           = field(default_factory=list)
    work_history:     List[dict]          = field(default_factory=list)
    source_file:      Optional[str]       = None   # PDF / DOCX filename

    def to_dict(self) -> dict:
        """Serialize candidate to flat dictionary for DataFrame storage."""
        return {
            "name":             self.name,
            "email":            self.email,
            "phone":            self.phone,
            "location":         self.location,
            "experience_years": self.experience_years,
            "education":        " | ".join(self.education),
            "skills":           ", ".join(self.skills),
            "certifications":   " | ".join(self.certifications),
            "projects":         " | ".join(self.projects),
            "source_file":      self.source_file,
        }

    def __repr__(self) -> str:
        return (
            f"Candidate(name={self.name!r}, "
            f"skills={self.skills}, "
            f"experience={self.experience_years}yrs)"
        )


# ── DataFrame Schema ───────────────────────────────────────────
CANDIDATE_SCHEMA = {
    "name":             "string",
    "email":            "string",
    "phone":            "string",
    "location":         "string",
    "experience_years": "float64",
    "education":        "string",
    "skills":           "string",
    "certifications":   "string",
    "projects":         "string",
    "source_file":      "string",
}


def candidates_to_dataframe(candidates: List[Candidate]) -> pd.DataFrame:
    """
    Convert a list of Candidate objects into a typed pandas DataFrame.

    Args:
        candidates: List of Candidate dataclass instances

    Returns:
        pd.DataFrame with one row per candidate
    """
    if not candidates:
        return pd.DataFrame(columns=list(CANDIDATE_SCHEMA.keys()))

    rows = [c.to_dict() for c in candidates]
    df = pd.DataFrame(rows)

    # Apply schema types where possible
    for col, dtype in CANDIDATE_SCHEMA.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except (ValueError, TypeError):
                pass  # keep original dtype if cast fails

    return df
