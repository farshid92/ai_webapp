import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import torch


def test_predict_endpoint_success(client: TestClient, sample_inputs, mock_model):
    """Test successful prediction request."""
    response = client.post(
        "/api/predict/",
        json={
            "inputs": sample_inputs,
            "model_name": "base"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model" in data
    assert data["model"] == "base"
    assert isinstance(data["prediction"], (int, float))


def test_predict_endpoint_default_model(client: TestClient, sample_inputs, mock_model):
    """Test prediction with default model name."""
    response = client.post(
        "/api/predict/",
        json={"inputs": sample_inputs}
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model" in data


def test_predict_endpoint_invalid_input(client: TestClient):
    """Test prediction with invalid input."""
    response = client.post(
        "/api/predict/",
        json={"inputs": "not a list"}
    )
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_empty_input(client: TestClient, mock_model):
    """Test prediction with empty input list."""
    response = client.post(
        "/api/predict/",
        json={"inputs": []}
    )
    # Should either succeed or return validation error
    assert response.status_code in [200, 422]


def test_predict_endpoint_missing_inputs(client: TestClient):
    """Test prediction with missing inputs field."""
    response = client.post(
        "/api/predict/",
        json={"model_name": "base"}
    )
    assert response.status_code == 422  # Validation error

