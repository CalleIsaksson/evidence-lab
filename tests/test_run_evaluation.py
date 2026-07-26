from pathlib import Path

import pytest

from scripts.run_evaluation import (
    DEFAULT_DATA_PATH,
    EvaluationData,
    calculate_metrics,
    evaluate_tfidf,
    evaluate_word_frequency,
    format_results_table,
    load_evaluation_data,
    prepare_evaluation_inputs,
)


def create_evaluation_data() -> EvaluationData:
    return {
        "name": "test_dataset",
        "description": "A small test dataset.",
        "chunk_size": 2,
        "chunks": [
            {"id": "password", "text": "password reset"},
            {"id": "vpn", "text": "vpn access"},
            {"id": "device", "text": "device return"},
        ],
        "queries": [
            {"query": "password", "relevant_chunk_id": "password"},
            {"query": "vpn", "relevant_chunk_id": "vpn"},
            {"query": "device", "relevant_chunk_id": "device"},
        ],
    }


def test_load_evaluation_data_reads_json(tmp_path: Path) -> None:
    evaluation_file = tmp_path / "evaluation.json"
    evaluation_file.write_text(
        '{"name": "test_dataset", "chunk_size": 25}',
        encoding="utf-8",
    )

    result = load_evaluation_data(evaluation_file)

    assert result == {
        "name": "test_dataset",
        "chunk_size": 25,
    }


def test_prepare_evaluation_inputs_builds_document_and_labels() -> None:
    data = create_evaluation_data()

    document, queries, relevant_chunks, chunk_size = (
        prepare_evaluation_inputs(data)
    )

    assert document == "password reset vpn access device return"
    assert queries == ["password", "vpn", "device"]
    assert relevant_chunks == [
        "password reset",
        "vpn access",
        "device return",
    ]
    assert chunk_size == 2


def test_evaluate_word_frequency_returns_expected_metrics() -> None:
    result = evaluate_word_frequency(create_evaluation_data())

    assert result == {
        "hit_rate_at_1": 1.0,
        "hit_rate_at_3": 1.0,
        "mean_reciprocal_rank": 1.0,
    }


def test_evaluate_tfidf_returns_expected_metrics() -> None:
    result = evaluate_tfidf(create_evaluation_data())

    assert result == {
        "hit_rate_at_1": 1.0,
        "hit_rate_at_3": 1.0,
        "mean_reciprocal_rank": 1.0,
    }


def test_prepare_evaluation_inputs_rejects_incorrect_chunk_size() -> None:
    data = create_evaluation_data()
    data["chunk_size"] = 3

    with pytest.raises(
        ValueError,
        match="evaluation chunks must match the configured chunk size",
    ):
        prepare_evaluation_inputs(data)


def test_real_evaluation_dataset_has_reproducible_results() -> None:
    data = load_evaluation_data(DEFAULT_DATA_PATH)

    assert evaluate_word_frequency(data) == pytest.approx(
        {
            "hit_rate_at_1": 0.6666666667,
            "hit_rate_at_3": 0.8333333333,
            "mean_reciprocal_rank": 0.7694444444,
        }
    )
    assert evaluate_tfidf(data) == pytest.approx(
        {
            "hit_rate_at_1": 0.8333333333,
            "hit_rate_at_3": 0.8333333333,
            "mean_reciprocal_rank": 0.8666666667,
        }
    )


def test_calculate_metrics_and_format_results_table() -> None:
    metrics = calculate_metrics(
        [
            ["first", "other", "last"],
            ["other", "second", "last"],
            ["other", "last", "third"],
            ["other", "last"],
        ],
        ["first", "second", "third", "missing"],
    )

    assert metrics["hit_rate_at_1"] == 0.25
    assert metrics["hit_rate_at_3"] == 0.75
    assert metrics["mean_reciprocal_rank"] == pytest.approx(
        (1.0 + 0.5 + (1 / 3)) / 4
    )
    assert format_results_table({"Test method": metrics}) == (
        "| Method | Hit Rate@1 | Hit Rate@3 | MRR |\n"
        "| --- | ---: | ---: | ---: |\n"
        "| Test method | 0.250 | 0.750 | 0.458 |"
    )
