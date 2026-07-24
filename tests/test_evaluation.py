from evidence_lab.evaluation import hit_at_k


def test_hit_at_k_returns_true_when_relevant_chunk_is_retrieved() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = hit_at_k(retrieved_chunks, "data dog")
    assert result is True


def test_hit_at_k_returns_false_when_relevant_chunk_is_not_retrieved() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = hit_at_k(retrieved_chunks, "cat sleeps")
    assert result is False
