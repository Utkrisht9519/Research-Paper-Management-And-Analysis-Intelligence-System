import requests
from config import WIKI_API

def wiki_lookup(term):
    res = requests.get(WIKI_API + term)
    if res.status_code != 200:
        return "No wiki result found"
    return res.json().get("extract", "")
