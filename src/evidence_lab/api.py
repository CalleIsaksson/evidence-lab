from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from evidence_lab.retrieval import retrieve_most_relevant_chunks


class RetrievalRequest(BaseModel):
    document: str = Field(min_length=1)
    query: str = Field(min_length=1)
    chunk_size: int = Field(gt=0)
    num_chunks: int = Field(default=1, gt=0)


class RetrievalResponse(BaseModel):
    best_chunks: list[str]


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
