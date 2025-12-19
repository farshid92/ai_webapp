import torch
from app.ml.model import RegressionNet

DEVICE = torch.device("cpu")

def load_model() -> RegressionNet:
    model = RegressionNet()
    model.eval()
    model.to(DEVICE)

    # Later:
    # model.load_state_dict(torch.load("weights.pt"))

    return model
