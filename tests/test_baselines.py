import pytest

from evidence_lab.baselines import rank_chunks_with_tfidf


def test_rank_chunks_with_tfidf_ranks_each_query() -> None:
    chunks = [
        "password reset instructions",
        "vpn access instructions",
        "device return instructions",
    ]

    results = rank_chunks_with_tfidf(
        chunks,
        ["vpn access", "return device"],
    )

    assert results[0][0] == "vpn access instructions"
    assert results[1][0] == "device return instructions"


def test_rank_chunks_with_tfidf_keeps_corpus_order_for_tied_scores() -> None:
    chunks = ["password reset", "vpn access", "device return"]

    results = rank_chunks_with_tfidf(chunks, ["unknown phrase"])

    assert results == [chunks]


def test_rank_chunks_with_tfidf_returns_empty_list_for_no_queries() -> None:
    assert rank_chunks_with_tfidf(["password reset"], []) == []


def test_rank_chunks_with_tfidf_rejects_empty_chunks() -> None:
    with pytest.raises(ValueError, match="chunks must contain text"):
        rank_chunks_with_tfidf([], ["password"])


def test_rank_chunks_with_tfidf_rejects_blank_query() -> None:
    with pytest.raises(ValueError, match="queries must contain text"):
        rank_chunks_with_tfidf(["password reset"], [" "])
