import requests
import streamlit as st
import json

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a careful academic research assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    response = requests.post(GROQ_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return f"❌ Groq error {response.status_code}: {response.text}"

    return response.json()["choices"][0]["message"]["content"]
