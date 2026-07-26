from pathlib import Path

from scripts.run_evaluation import load_evaluation_data


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
