import torch
from app.ml.registry import get_model
from app.ml.loader import DEVICE
from app.ml.base import BaseModel


def predict(model: BaseModel, inputs: list[float]) -> float:
    input_dim = len(inputs)
    
    # Ensure input tensor has correct shape: (batch_size, input_dim)
    x = torch.tensor(inputs, dtype=torch.float32).unsqueeze(0).to(DEVICE)
    
    # Check if model input dimension matches
    # Get the first layer's input size
    if hasattr(model, 'net') and len(model.net) > 0:
        first_layer = model.net[0]
        if hasattr(first_layer, 'in_features'):
            expected_dim = first_layer.in_features
            if input_dim != expected_dim:
                raise ValueError(
                    f"Input dimension mismatch: received {input_dim} values, "
                    f"but model expects {expected_dim} inputs. "
                    f"Please provide exactly {expected_dim} comma-separated numbers."
                )

    with torch.no_grad():
        y = model.predict(x)

    return float(y.item())
