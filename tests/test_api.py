from fastapi.testclient import TestClient

from evidence_lab.api import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_retrieve_returns_best_chunk() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover hund springer",
            "query": "hund",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"best_chunk": "hund springer"}

def test_retrieve_rejects_empty_query() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": "",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "query must contain text"}