import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.ml.model import RegressionNet
import torch


@pytest.fixture
def mock_model():
    """Create a mock model for testing."""
    model = RegressionNet(input_dim=4)
    model.eval()
    # Mock the predict method to return a fixed value
    original_predict = model.predict
    
    def mock_predict(x):
        # Return a simple sum of inputs for testing
        return torch.tensor([[sum(x[0].tolist())]], dtype=torch.float32)
    
    model.predict = mock_predict
    return model


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_inputs():
    """Sample input data for testing."""
    return [1.0, 2.0, 3.0, 4.0]


@pytest.fixture(autouse=True)
def mock_model_loading(mock_model):
    """Automatically mock model loading for all tests."""
    # Patch at multiple levels to ensure it works
    with patch('app.ml.loader.load_model', return_value=mock_model):
        with patch('app.ml.registry.load_model', return_value=mock_model):
            with patch('app.ml.registry.get_model', return_value=mock_model):
                # Mock the registry instance methods
                with patch('app.api.models.get_registry') as mock_get_registry:
                    registry_mock = MagicMock()
                    registry_mock.get.return_value = mock_model
                    registry_mock.list_models.return_value = ["base"]
                    registry_mock.info.return_value = {
                        "name": "base",
                        "version": "0.1",
                        "type": "RegressionNet"
                    }
                    registry_mock.load = MagicMock()
                    mock_get_registry.return_value = registry_mock
                    yield

