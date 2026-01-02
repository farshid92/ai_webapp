import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_method_not_allowed(client: TestClient):
    """Test that POST is not allowed on health endpoint."""
    response = client.post("/health")
    assert response.status_code == 405  # Method Not Allowed

