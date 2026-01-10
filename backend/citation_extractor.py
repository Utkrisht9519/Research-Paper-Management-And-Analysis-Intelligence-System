import re
import json
from config import CITATION_DB

def extract_references(text):
    refs = re.split(r"\n\d+\.\s|\n\[\d+\]\s", text)
    return [r.strip() for r in refs if len(r.strip()) > 30]

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
        return json.load(f).get(paper_id, [])
