"""
backend/nlp_extractor.py
========================
Dynamic NLP Skill Extractor — Part 2, Milestone 2
Uses HuggingFace transformers to extract skills dynamically.
"""

from typing import List
import re

try:
    from transformers import pipeline
    # We use a general NER model or a specific skill-extraction model if available.
    # dslim/bert-base-NER is good for generic entities.
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
except ImportError:
    print("WARNING: 'transformers' or 'torch' not installed. NLP extractor will not work.")
    ner_pipeline = None

def extract_skills_nlp(text: str) -> List[str]:
    """
    Extract skills dynamically from text using a pre-trained NLP model.
    This goes beyond simple keyword matching to find skills we might not
    have in our hardcoded list.

    Args:
        text: Raw resume or job description text.

    Returns:
        List of extracted skill strings.
    """
    if not ner_pipeline or not text:
        return []

    try:
        # Keep text length reasonable for BERT (max 512 tokens usually)
        # We'll just process the first 2000 chars as a heuristic for now
        short_text = text[:2000]
        entities = ner_pipeline(short_text)
        
        skills = []
        for e in entities:
            # Often technical skills get tagged as MISC or ORG by generic NER models
            if e.get("entity_group") in ["MISC", "ORG"]:
                word = e.get("word", "")
                # Clean up subword artifacts like '##' from WordPiece tokenization
                word = word.replace("##", "")
                # Filter out very short or non-alphabetical artifacts
                if len(word) > 2 and re.match(r'^[A-Za-z0-9+#]+$', word):
                    skills.append(word)
                    
        return list(set(skills))
    except Exception as ex:
        print(f"NLP Extraction Error: {ex}")
        return []

if __name__ == "__main__":
    sample_text = "I have extensive experience working with PyTorch, Kubernetes, and Apache Kafka."
    print("Testing NLP Extractor:")
    skills = extract_skills_nlp(sample_text)
    print(f"Extracted: {skills}")
