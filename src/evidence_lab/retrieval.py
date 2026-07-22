from evidence_lab.chunking import chunk_text
from evidence_lab.similarity import cosine_similarity, word_frequencies


def retrieve_most_relevant_chunk(
    document: str,
    query: str,
    chunk_size: int,
) -> str:
    chunks = chunk_text(document, chunk_size)

    if not chunks:
        raise ValueError("document must contain text")
    if not query.strip():
        raise ValueError("query must contain text")

    query_frequencies = word_frequencies(query)
    scores: list[float] = []

    for chunk in chunks:
        chunk_frequencies = word_frequencies(chunk)
        score = cosine_similarity(chunk_frequencies, query_frequencies)
        scores.append(score)

    best_score = max(scores)
    best_index = scores.index(best_score)
    best_chunk = chunks[best_index]

    return best_chunk
