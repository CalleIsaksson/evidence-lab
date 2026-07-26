# EvidenceLab

EvidenceLab is a portfolio project for classical information retrieval and retrieval evaluation.

The project:

* splits documents into word-based chunks
* represents chunks and queries using word-frequency vectors
* compares chunks with a query using cosine similarity
* returns the most relevant chunks in ranked order
* provides retrieval through both a command-line interface and a REST API
* evaluates multiple searches using two metrics: Hit Rate and Mean Reciprocal Rank (MRR)

## Start the program

Activate the virtual environment and run the following command from the project folder in PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m evidence_lab.main
```

Example input:

```text
Document: cat sleeps dog runs
Query: dog
Chunk size: 2
Number of Chunks: 1
Most relevant chunks: ['dog runs']
```

## Start the REST API

Run the following command from the project folder in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m uvicorn evidence_lab.api:app --app-dir src --reload
```

The API is then available at:

* http://127.0.0.1:8000
* interactive documentation: http://127.0.0.1:8000/docs

Here we create a PowerShell object containing `document`, `query`, `chunk_size` and `num_chunks`. The object is then converted to JSON format.

```powershell
$body = @{
    document = "cat sleeps dog runs"
    query = "dog"
    chunk_size = 2
    num_chunks = 1
} | ConvertTo-Json
```

The JSON data is then sent to `POST /retrieve` using `Invoke-RestMethod`.

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/retrieve" `
    -ContentType "application/json" `
    -Body $body
```

Running the command returns:

```text
best_chunks
-----------
{dog runs}
```

Here we create a PowerShell object containing `document`, `queries`, `relevant_chunks`, `chunk_size` and `num_chunks`. The object is then converted to JSON format.

The endpoint runs multiple queries against the same document and evaluates the quality of the retrieval using two metrics, Hit Rate and Mean Reciprocal Rank (MRR).

```powershell
$evaluationBody = @{
    document = "dog runs cat sleeps"
    queries = @("dog", "cat")
    relevant_chunks = @("dog runs", "cat sleeps")
    chunk_size = 2
    num_chunks = 1
} | ConvertTo-Json
```

The JSON data is then sent to `POST /evaluate` using `Invoke-RestMethod`.

```powershell
Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/evaluate" `
    -ContentType "application/json" `
    -Body $evaluationBody |
    ConvertTo-Json
```

Running the command returns:

```json
{
  "hit_rate": 1.0,
  "mean_reciprocal_rank": 1.0
}
```

## Run the tests

```powershell
python -m pytest
```

## Technology choices

* **FastAPI** is used to receive and validate HTTP requests containing JSON data.
* **Uvicorn** runs the FastAPI application as a local web server.
* **HTTPX** is used by the API tests to send test requests without manually starting the server.

The project uses these small and focused tools instead of a larger web framework. The retrieval logic remains regular Python and can be used without the REST API.
