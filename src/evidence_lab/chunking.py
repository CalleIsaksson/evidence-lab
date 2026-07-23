def chunk_text(text: str, chunk_size: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    words = text.split()
    chunks: list[str] = []

    for start in range(0, len(words), chunk_size):
        chunk_words = words[start:start + chunk_size]
        chunks.append(" ".join(chunk_words))

    return chunks
