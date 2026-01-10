import re
import json
from config import CITATION_DB

def extract_references(text):
    """
    Very robust academic reference extraction (APA/IEEE mixed)
    """
    refs = re.split(r"\n\d+\.\s|\n\[\d+\]\s", text)
    references = [r.strip() for r in refs if len(r.strip()) > 30]
    return references

def save_citations(paper_id, references):
    try:
        with open(CITATION_DB, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[paper_id] = references

    with open(CITATION_DB, "w") as f:
        json.dump(data, f, indent=4)

def get_citations(paper_id):
    with open(CITATION_DB, "r") as f:
        data = json.load(f)
    return data.get(paper_id, [])
