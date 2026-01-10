from groq import Groq
from config import LLM_MODEL


def answer_query(query, context):
    client = Groq()
    prompt = f"""
    Use the context to answer.
    Cite sources where possible.

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
    model=LLM_MODEL,
    messages=[{"role": "user", "content": prompt}],
)

    return response.choices[0].message.content
