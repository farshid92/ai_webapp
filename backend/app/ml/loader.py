import torch
from pathlib import Path
from app.ml.model import RegressionNet

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# default checkpoint (for now)
ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DIR = ROOT / "ml" / "checkpoints" / "base.pt"


def load_model(
    checkpoint_name: str = "base.pt",
    input_dim: int = 3,
) -> RegressionNet:
    checkpoint_path = CHECKPOINT_DIR / checkpoint_name

    model = RegressionNet(input_dim=input_dim)
    model.load_state_dict(
        torch.load(checkpoint_path, map_location=DEVICE)
    )
    model.to(DEVICE)
    model.eval()

    return model
