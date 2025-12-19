import torch
import numpy as np
from app.ml.loader import DEVICE

def predict(model, inputs: list[float]) -> float:
    x = torch.tensor(inputs, dtype=torch.float32).unsqueeze(0)
    x = x.to(DEVICE)

    with torch.no_grad():
        y = model(x)

    return float(y.item())
