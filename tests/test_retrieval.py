import pytest


from evidence_lab.retrieval import retrieve_most_relevant_chunk


def test_retrieve_most_relevant_chunk_finds_matching_chunk() -> None:
    document = "katt sover hund springer"

    result = retrieve_most_relevant_chunk(
        document,
        query="hund",
        chunk_size=2,
    )

    assert result == "hund springer"


def test_retrieve_rejects_empty_query() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunk("katt sover", "", 2)


def test_retrieve_rejects_empty_document() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunk("", "hej", 2)
