import pytest


from evidence_lab.similarity import cosine_similarity, word_frequencies


def test_word_frequencies_counts_words() -> None:
    result = word_frequencies("hund katt hund")

    assert result == {"hund": 2, "katt": 1}


def test_word_frequencies_returns_empty_dict_for_empty_text() -> None:
    result = word_frequencies("")

    assert result == {}


def test_word_frequencies_normalizes_case_and_punctuation() -> None:
    result = word_frequencies("Hund, hund. HUND!")

    assert result == {"hund": 3}


def test_cosine_similarity_is_one_for_identical_vectors() -> None:
    result = cosine_similarity(
        {"hund": 2, "katt": 1},
        {"hund": 2, "katt": 1},
    )

    assert result == pytest.approx(1.0)


def test_cosine_similarity_is_zero_without_shared_words() -> None:
    result = cosine_similarity(
        {"hund": 1},
        {"katt": 1},
    )

    assert result == 0.0
