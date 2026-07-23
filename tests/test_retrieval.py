import pytest

from evidence_lab.retrieval import retrieve_most_relevant_chunks


def test_retrieve_most_relevant_chunks_finds_matching_chunk() -> None:
    document = "katt sover hund springer"

    result = retrieve_most_relevant_chunks(
        document,
        query="hund",
        chunk_size=2,
    )

    assert result == ["hund springer"]


def test_retrieve_rejects_empty_query() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunks("katt sover", "", 2)


def test_retrieve_rejects_empty_document() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunks("", "hej", 2)


def test_ranked_retrieval_works() -> None:
    document = "hund heter hund och hund äter men musmattan är svart och inte så fin"

    result = retrieve_most_relevant_chunks(
        document,
        query="hund",
        chunk_size=3,
        num_chunks=2,
    )

    assert result == ["hund heter hund", "och hund äter"]


def test_retrieve_rejects_non_positive_num_chunks() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunks("katt sover", "katt", 2, 0)
