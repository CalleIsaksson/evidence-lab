import json
from pathlib import Path
from typing import TypedDict, cast

from evidence_lab.evaluation import hit_rate_at_k, mean_reciprocal_rank
from evidence_lab.retrieval import retrieve_most_relevant_chunks


class EvaluationChunk(TypedDict):
    id: str
    text: str


class EvaluationQuery(TypedDict):
    query: str
    relevant_chunk_id: str


class EvaluationData(TypedDict):
    name: str
    description: str
    chunk_size: int
    chunks: list[EvaluationChunk]
    queries: list[EvaluationQuery]


class EvaluationMetrics(TypedDict):
    hit_rate_at_1: float
    hit_rate_at_3: float
    mean_reciprocal_rank: float


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "evaluation.json"


def load_evaluation_data(path: Path) -> EvaluationData:
    with path.open(encoding="utf-8") as file:
        return cast(EvaluationData, json.load(file))


def prepare_evaluation_inputs(
    data: EvaluationData,
) -> tuple[str, list[str], list[str], int]:
    chunks_by_id = {
        chunk["id"]: chunk["text"]
        for chunk in data["chunks"]
    }
    document = " ".join(chunk["text"] for chunk in data["chunks"])
    queries = [item["query"] for item in data["queries"]]
    relevant_chunks = [
        chunks_by_id[item["relevant_chunk_id"]]
        for item in data["queries"]
    ]

    return document, queries, relevant_chunks, data["chunk_size"]


def calculate_metrics(
    retrieved_results: list[list[str]],
    relevant_chunks: list[str],
) -> EvaluationMetrics:
    top_one_results = [results[:1] for results in retrieved_results]
    top_three_results = [results[:3] for results in retrieved_results]

    return {
        "hit_rate_at_1": hit_rate_at_k(top_one_results, relevant_chunks),
        "hit_rate_at_3": hit_rate_at_k(top_three_results, relevant_chunks),
        "mean_reciprocal_rank": mean_reciprocal_rank(
            retrieved_results,
            relevant_chunks,
        ),
    }


def evaluate_word_frequency(data: EvaluationData) -> EvaluationMetrics:
    document, queries, relevant_chunks, chunk_size = (
        prepare_evaluation_inputs(data)
    )
    num_chunks = len(data["chunks"])
    retrieved_results = [
        retrieve_most_relevant_chunks(
            document,
            query,
            chunk_size,
            num_chunks,
        )
        for query in queries
    ]

    return calculate_metrics(retrieved_results, relevant_chunks)


def format_results_table(
    results: dict[str, EvaluationMetrics],
) -> str:
    lines = [
        "| Method | Hit Rate@1 | Hit Rate@3 | MRR |",
        "| --- | ---: | ---: | ---: |",
    ]

    for method, metrics in results.items():
        lines.append(
            f"| {method} "
            f"| {metrics['hit_rate_at_1']:.3f} "
            f"| {metrics['hit_rate_at_3']:.3f} "
            f"| {metrics['mean_reciprocal_rank']:.3f} |"
        )

    return "\n".join(lines)


def main() -> None:
    data = load_evaluation_data(DEFAULT_DATA_PATH)
    results = {
        "Word frequency + cosine": evaluate_word_frequency(data),
    }
    print(format_results_table(results))


if __name__ == "__main__":
    main()
