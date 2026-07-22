from evidence_lab.retrieval import retrieve_most_relevant_chunk
import pytest


def test_retrieve_most_relevant_chunk_finds_matching_chunk() -> None:
    document = "katt sover hund springer"

    result = retrieve_most_relevant_chunk(
        document,
        query="hund",
        chunk_size=2,
    )

    assert result == "hund springer"

def test_empty_query() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunk('katt sover', '', 2)

def test_document_must_contain_text() -> None:
    with pytest.raises(ValueError):
        retrieve_most_relevant_chunk('', 'hej', 2)
