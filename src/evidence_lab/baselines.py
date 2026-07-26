from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_chunks_with_tfidf(
    chunks: list[str],
    queries: list[str],
) -> list[list[str]]:
    if not chunks or not any(chunk.strip() for chunk in chunks):
        raise ValueError("chunks must contain text")
    if any(not query.strip() for query in queries):
        raise ValueError("queries must contain text")
    if not queries:
        return []

    vectorizer = TfidfVectorizer()
    chunk_vectors = vectorizer.fit_transform(chunks)
    query_vectors = vectorizer.transform(queries)
    scores = cosine_similarity(query_vectors, chunk_vectors)
    ranked_results: list[list[str]] = []

    for query_scores in scores:
        ranked_indices = sorted(
            range(len(chunks)),
            key=lambda index: (-query_scores[index], index),
        )
        ranked_results.append([chunks[index] for index in ranked_indices])

    return ranked_results
