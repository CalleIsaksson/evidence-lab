import pytest

from evidence_lab.evaluation import (
    hit_at_k,
    mean_reciprocal_rank,
    reciprocal_rank,
)


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


def test_mean_reciprocal_rank_rejects_lists_with_different_lengths() -> None:
    retrieved_results = [
        ["hund springer", "katt sover"],
    ]
    relevant_chunks = [
        "hund springer",
        "katt sover",
    ]

    with pytest.raises(ValueError):
        mean_reciprocal_rank(retrieved_results, relevant_chunks)


def test_mean_reciprocal_rank_averages_search_results() -> None:
    retrieved_results = [
        ["hund sover", "katt äter"],
        ["hund sover", "katt äter"],
    ]
    relevant_chunks = ["hund sover", "katt äter"]

    result = mean_reciprocal_rank(retrieved_results, relevant_chunks)
    assert result == 0.75


def test_mean_reciprocal_rank_gives_zero_for_empty_lists() -> None:
    retrieved_results = []
    relevant_chunks = []

    result = mean_reciprocal_rank(retrieved_results, relevant_chunks)
    assert result == 0.0
