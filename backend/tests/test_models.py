import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


def test_list_models_endpoint(client: TestClient):
    """Test listing available models."""
    response = client.get("/api/models/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "base" in data


def test_model_info_endpoint_success(client: TestClient):
    """Test getting model info for existing model."""
    response = client.get("/api/models/base")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "type" in data
    assert data["name"] == "base"


def test_model_info_endpoint_not_found(client: TestClient):
    """Test getting info for non-existent model."""
    from unittest.mock import patch
    
    # Mock the registry to return None for non-existent model
    with patch('app.api.models.get_registry') as mock_get_registry:
        registry_mock = MagicMock()
        registry_mock.info.return_value = None  # Model not found
        mock_get_registry.return_value = registry_mock
        
        response = client.get("/api/models/nonexistent")
        assert response.status_code == 404
        assert "detail" in response.json()
        assert "not found" in response.json()["detail"].lower()

