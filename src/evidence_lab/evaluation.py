def hit_at_k(
    retrieved_chunks: list[str],
    relevant_chunk: str,
) -> bool:
    for chunk in retrieved_chunks:
        if chunk == relevant_chunk:
            return True

    return False


def hit_rate_at_k(
    retrieved_results: list[list[str]],
    relevant_chunks: list[str],
) -> float:
    if len(retrieved_results) != len(relevant_chunks):
        raise ValueError(
            "retrieved results and relevant chunks must have the same length"
        )

    if not retrieved_results:
        return 0.0

    hits = 0

    for index in range(len(retrieved_results)):
        if hit_at_k(retrieved_results[index], relevant_chunks[index]):
            hits += 1

    return hits / len(retrieved_results)


def reciprocal_rank(
    retrieved_chunks: list[str],
    relevant_chunk: str,
) -> float:
    position = 1

    for chunk in retrieved_chunks:
        if chunk == relevant_chunk:
            return 1 / position

        position += 1

    return 0.0


def mean_reciprocal_rank(
    retrieved_results: list[list[str]],
    relevant_chunks: list[str],
) -> float:
    if len(retrieved_results) != len(relevant_chunks):
        raise ValueError(
            "retrieved results and relevant chunks must have the same length"
        )

    if not retrieved_results:
        return 0.0

    total = 0.0

    for index in range(len(retrieved_results)):
        total += reciprocal_rank(
            retrieved_results[index],
            relevant_chunks[index],
        )

    return total / len(retrieved_results)
