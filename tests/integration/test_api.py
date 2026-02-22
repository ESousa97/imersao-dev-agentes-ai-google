from fastapi.testclient import TestClient

from src.botinho.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_endpoint_accepts_legacy_payload():
    response = client.post("/api/chat", json={"mensagem": "Como resetar senha?"})

    assert response.status_code == 200
    payload = response.json()
    assert "response" in payload
    assert "session_id" in payload
