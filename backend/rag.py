from groq import Groq

def answer_query(query, context_chunks):
    client = Groq()
    context = "\n".join(context_chunks)

    prompt = f"""
    Answer the question using the context below.
    Cite sources explicitly.

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
