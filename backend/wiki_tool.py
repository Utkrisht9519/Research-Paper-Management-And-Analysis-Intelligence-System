import requests
from config import WIKI_API

def wiki_lookup(term):
    response = requests.get(WIKI_API + term)
    if response.status_code != 200:
        return "No wiki information found."

    data = response.json()
    return data.get("extract", "No summary available.")
