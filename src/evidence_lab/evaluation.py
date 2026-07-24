def hit_at_k(
    retrieved_chunks: list[str],
    relevant_chunk: str,
) -> bool:
    for chunk in retrieved_chunks:
        if chunk == relevant_chunk:
            return True

    return False
