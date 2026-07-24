def hit_at_k(
    retrieved_chunks: list[str],
    relevant_chunk: str,
) -> bool:
    for chunk in retrieved_chunks:
        if chunk == relevant_chunk:
            return True

    return False


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
