from fastapi import FastAPI


app = FastAPI(title="EvidenceLab")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}