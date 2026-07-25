from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from evidence_lab.evaluation import evaluate_retrieval
from evidence_lab.retrieval import retrieve_most_relevant_chunks


class RetrievalRequest(BaseModel):
    document: str = Field(min_length=1)
    query: str = Field(min_length=1)
    chunk_size: int = Field(gt=0)
    num_chunks: int = Field(default=1, gt=0)


class RetrievalResponse(BaseModel):
    best_chunks: list[str]


class EvaluationRequest(BaseModel):
    document: str = Field(min_length=1)
    queries: list[str] = Field(min_length=1)
    relevant_chunks: list[str] = Field(min_length=1)
    chunk_size: int = Field(gt=0)
    num_chunks: int = Field(default=1, gt=0)


class EvaluationResponse(BaseModel):
    hit_rate: float
    mean_reciprocal_rank: float


app = FastAPI(title="EvidenceLab")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/retrieve")
def retrieve(request: RetrievalRequest) -> RetrievalResponse:
    try:
        best_chunks = retrieve_most_relevant_chunks(
            request.document,
            request.query,
            request.chunk_size,
            request.num_chunks,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return RetrievalResponse(best_chunks=best_chunks)


@app.post("/evaluate")
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    try:
        metrics = evaluate_retrieval(
            request.document,
            request.queries,
            request.relevant_chunks,
            request.chunk_size,
            request.num_chunks,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return EvaluationResponse(
        hit_rate=metrics["hit_rate"],
        mean_reciprocal_rank=metrics["mean_reciprocal_rank"],
    )
