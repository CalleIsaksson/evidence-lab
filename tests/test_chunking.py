import pytest


from evidence_lab.chunking import chunk_text


def test_chunk_text_splits_text_into_equal_parts() -> None:
    text = "ett två tre fyra"

    result = chunk_text(text, chunk_size=2)

    assert result == ["ett två", "tre fyra"]


def test_chunk_text_keeps_smaller_final_chunk() -> None:
    text = "ett två tre fyra fem"

    result = chunk_text(text, chunk_size=2)

    assert result == ["ett två", "tre fyra", "fem"]


def test_chunk_text_returns_empty_list_for_empty_text() -> None:
    result = chunk_text("", chunk_size=2)

    assert result == []


def test_chunk_text_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError):
        chunk_text("ett två", chunk_size=0)


def test_chunk_text_handles_chunk_size_larger_than_text() -> None:
    result = chunk_text("ett två", chunk_size=5)

    assert result == ["ett två"]
