from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from evidence_lab.retrieval import retrieve_most_relevant_chunk


class RetrievalRequest(BaseModel):
    document: str = Field(min_length=1)
    query: str = Field(min_length=1)
    chunk_size: int = Field(gt=0)


app = FastAPI(title="EvidenceLab")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/retrieve")
def retrieve(request: RetrievalRequest) -> dict[str, str]:
    try:
        best_chunk = retrieve_most_relevant_chunk(
            request.document,
            request.query,
            request.chunk_size,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"best_chunk": best_chunk}
