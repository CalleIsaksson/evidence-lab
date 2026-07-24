from evidence_lab.evaluation import hit_at_k, reciprocal_rank


def test_hit_at_k_returns_true_when_relevant_chunk_is_retrieved() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = hit_at_k(retrieved_chunks, "data dog")
    assert result is True


def test_hit_at_k_returns_false_when_relevant_chunk_is_not_retrieved() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = hit_at_k(retrieved_chunks, "cat sleeps")
    assert result is False


def test_reciprocal_rank_returns_one_for_first_position() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = reciprocal_rank(retrieved_chunks, "data dog")
    assert result == 1.0


def test_reciprocal_rank_returns_half_for_second_position() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = reciprocal_rank(retrieved_chunks, "did i")
    assert result == 0.5


def test_reciprocal_rank_returns_zero_when_relevant_chunk_is_not_retrieved() -> None:
    retrieved_chunks = ["data dog", "did i", "do that"]
    result = reciprocal_rank(retrieved_chunks, "gosh darnit")
    assert result == 0.0
