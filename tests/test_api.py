from fastapi.testclient import TestClient

from evidence_lab.api import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_retrieve_returns_best_chunks() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover hund springer",
            "query": "hund",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"best_chunks": ["hund springer"]}


def test_retrieve_returns_ranked_chunks() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "hund heter hund och hund äter men musmattan är svart och inte så fin",
            "query": "hund",
            "chunk_size": 3,
            "num_chunks": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_chunks": ["hund heter hund", "och hund äter"]
    }


def test_retrieve_rejects_empty_query() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": "",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 422


def test_retrieve_rejects_space_query() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": " ",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "query must contain text"}


def test_retrieve_rejects_non_positive_chunk_size() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": "katt",
            "chunk_size": 0,
        },
    )

    assert response.status_code == 422


def test_retrieve_rejects_empty_document() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "",
            "query": "katt",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 422


def test_retrieve_rejects_space_document() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": " ",
            "query": "katt",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "document must contain text"}


def test_retrieve_rejects_no_query() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "chunk_size": 2,
        },
    )
    assert response.status_code == 422


def test_retrieve_rejects_no_document() -> None:
    response = client.post(
        "/retrieve",
        json={
            "query": "dog",
            "chunk_size": 2,
        },
    )

    assert response.status_code == 422


def test_retrieve_rejects_no_chunk_size() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": "dog",
        },
    )

    assert response.status_code == 422


def test_retrieve_rejects_non_positive_num_chunks() -> None:
    response = client.post(
        "/retrieve",
        json={
            "document": "katt sover",
            "query": "dog",
            "chunk_size": 2,
            "num_chunks": 0,
        },
    )

    assert response.status_code == 422
