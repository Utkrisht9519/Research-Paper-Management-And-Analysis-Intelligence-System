def chunk_text(text, chunk_size=800, overlap=200):
    chunks = []

    # Force first chunk to be beginning of paper (abstract + intro)
    chunks.append(text[:1500])

    start = 1500
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
