from fastapi.testclient import TestClient
from main import app


def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_listar_empresas():
    response = TestClient(app).get("/api/v1/empresas")
    assert response.status_code == 200
    assert "empresas" in response.json()


def test_dashboard():
    response = TestClient(app).get("/api/v1/dashboard/resumo")
    assert response.status_code == 200
    assert "empresas" in response.json()
