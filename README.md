# EvidenceLab

[![Tests](https://github.com/CalleIsaksson/evidence-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/CalleIsaksson/evidence-lab/actions/workflows/tests.yml)

EvidenceLab is a small, transparent information retrieval project built to
demonstrate document chunking, ranking, API design, automated testing, and
reproducible retrieval evaluation.

The project deliberately uses classical information retrieval rather than
embeddings or large language models. This makes the ranking logic easy to
inspect and provides a baseline for future semantic retrieval work.

## Features

* splits documents into fixed-size word chunks
* represents chunks and queries with word-frequency vectors
* ranks chunks with cosine similarity
* compares the custom method with a TF-IDF baseline
* exposes retrieval and evaluation through a FastAPI REST API
* provides a command-line interface
* evaluates ranked results with Hit Rate@1, Hit Rate@3, and MRR
* runs 61 automated tests locally and in GitHub Actions

## Architecture

The main retrieval flow has four steps:

1. Split the input document into word-based chunks.
2. Convert each chunk and query into a vector representation.
3. Calculate cosine similarity and rank the chunks by relevance.
4. Evaluate the rankings against labeled relevant chunks.

EvidenceLab includes two retrieval methods:

* **Word frequency + cosine** is implemented from scratch and powers the CLI
  and REST API.
* **TF-IDF + cosine** uses scikit-learn as an established comparison baseline.

The reproducible evaluation script runs both methods against the same dataset
and uses the same metrics for a fair comparison.

## Installation

Clone the repository and open the project folder:

```powershell
git clone https://github.com/CalleIsaksson/evidence-lab.git
cd evidence-lab
```

Create and activate a virtual environment, then install the project and its
development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Command-line usage

Run the interactive program from the project folder:

```powershell
python -m evidence_lab.main
```

Example:

```text
Document: Password reset links expire after fifteen minutes. VPN access requires company authentication.
Query: VPN authentication
Chunk size: 7
Number of Chunks: 1
Most relevant chunks: ['VPN access requires company authentication.']
```

## REST API

Start the local API server:

```powershell
python -m uvicorn evidence_lab.api:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive OpenAPI
documentation at `http://127.0.0.1:8000/docs`.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check whether the API is running. |
| `POST` | `/retrieve` | Return ranked chunks for one query. |
| `POST` | `/evaluate` | Evaluate several queries against labeled chunks. |

### Retrieve relevant chunks

Create a JSON request body in PowerShell:

```powershell
$body = @{
    document = "Password reset links expire quickly. VPN access requires company authentication."
    query = "VPN authentication"
    chunk_size = 5
    num_chunks = 1
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/retrieve" `
    -ContentType "application/json" `
    -Body $body |
    ConvertTo-Json
```

Response:

```json
{
  "best_chunks": [
    "VPN access requires company authentication."
  ]
}
```

### Evaluate retrieval

```powershell
$evaluationBody = @{
    document = "Password reset links expire quickly. VPN access requires company authentication."
    queries = @("reset links", "VPN authentication")
    relevant_chunks = @(
        "Password reset links expire quickly.",
        "VPN access requires company authentication."
    )
    chunk_size = 5
    num_chunks = 1
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/evaluate" `
    -ContentType "application/json" `
    -Body $evaluationBody |
    ConvertTo-Json
```

Response:

```json
{
  "hit_rate": 1.0,
  "mean_reciprocal_rank": 1.0
}
```

## Reproducible evaluation

The synthetic IT-support dataset in
[`data/evaluation.json`](data/evaluation.json) contains eight labeled chunks of
25 words and 12 queries. It includes direct keyword queries and paraphrased
queries that expose the limits of lexical retrieval.

Run both retrieval methods against the same dataset:

```powershell
python scripts/run_evaluation.py
```

Results:

| Method | Hit Rate@1 | Hit Rate@3 | MRR |
| --- | ---: | ---: | ---: |
| Word frequency + cosine | 0.667 | 0.833 | 0.769 |
| TF-IDF + cosine | 0.833 | 0.833 | 0.867 |

* **Hit Rate@1** is the fraction of queries with the relevant chunk ranked
  first.
* **Hit Rate@3** is the fraction with the relevant chunk among the first three
  results.
* **MRR** averages the reciprocal rank of the first relevant result.

TF-IDF improves first-position accuracy and MRR on this dataset. Both methods
remain lexical, so neither can reliably solve queries expressed only through
unseen synonyms.

## Testing and continuous integration

Run the complete test suite:

```powershell
python -m pytest
```

GitHub Actions performs a clean installation, runs all tests, and executes the
evaluation script on every push and pull request.

## Limitations

* Fixed-size word chunking does not follow sentence or paragraph boundaries.
* Both retrieval methods depend on lexical overlap and do not understand
  meaning in the way embedding models do.
* The evaluation dataset is small and synthetic, so the results demonstrate
  the workflow rather than general retrieval performance.
* Zero-similarity ties keep corpus order, which can slightly improve rank-based
  metrics for unmatched queries.
* All chunks are ranked in memory; there is no persistent search index.
* The project does not include an LLM or answer-generation step and is not a
  complete RAG system.

## Technology choices

* **Python** implements the retrieval and evaluation logic.
* **FastAPI** validates HTTP requests and exposes the REST API.
* **Uvicorn** runs the local ASGI server.
* **scikit-learn** provides the TF-IDF comparison baseline.
* **Pytest** and **HTTPX** test the Python logic and API behavior.
* **GitHub Actions** runs the project in a clean CI environment.

## Future work

Natural extensions include a larger evaluation corpus, semantic embeddings,
an indexed document store, and an optional LLM generation step grounded in the
retrieved chunks.
