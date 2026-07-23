from evidence_lab.chunking import chunk_text
from evidence_lab.similarity import cosine_similarity, word_frequencies


def retrieve_most_relevant_chunks(
    document: str,
    query: str,
    chunk_size: int,
    num_chunks: int = 1,
) -> list[str]:
    chunks = chunk_text(document, chunk_size)

    if not chunks:
        raise ValueError("document must contain text")
    if not query.strip():
        raise ValueError("query must contain text")
    if num_chunks < 1:
        raise ValueError("number of chunks must be greater than 0")

    query_frequencies = word_frequencies(query)
    scores: dict[str, float] = {}

    for chunk in chunks:
        chunk_frequencies = word_frequencies(chunk)
        score = cosine_similarity(chunk_frequencies, query_frequencies)
        scores[chunk] = score

    ranked_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _score in ranked_scores[:num_chunks]]
