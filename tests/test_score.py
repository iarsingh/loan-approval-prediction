from fastapi.testclient import TestClient
from loans.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'income': 120000, 'debt_ratio': 0.1, 'credit_months': 48}).json()["label"]
    high = client.post("/score", json={'income': 120000, 'debt_ratio': 0.1, 'credit_months': 48}).json()
    low = client.post("/score", json={'income': 20000, 'debt_ratio': 0.8, 'credit_months': 2}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'income': 120000, 'debt_ratio': 0.1, 'credit_months': 48})
    body.pop("income")
    assert client.post("/score", json=body).status_code == 422
