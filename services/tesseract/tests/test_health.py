from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status_returns_engine_info():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "tesseract"
    assert data["status"] in ("ready", "unavailable")
    assert "version" in data
    assert isinstance(data["version"], str)
