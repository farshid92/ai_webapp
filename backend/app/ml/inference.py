import torch
from app.ml.registry import get_model
from app.ml.loader import DEVICE


def predict(model_name: str, inputs: list[float]) -> float:
    model = get_model(model_name)

    x = torch.tensor(inputs, dtype=torch.float32).unsqueeze(0)
    x = x.to(DEVICE)

    with torch.no_grad():
        y = model(x)

    return float(y.item())
