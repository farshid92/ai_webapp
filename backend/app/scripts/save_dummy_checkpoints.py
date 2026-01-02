import torch
from app.ml.model import RegressionNet
from pathlib import Path

# Resolve checkpoint directory - relative to app/ml/loader.py location
# This script is in app/scripts/, so parents[1] is app/
CHECKPOINT_DIR = Path(__file__).resolve().parent.parent / "ml" / "checkpoints"
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

model = RegressionNet(input_dim=3)

checkpoint_path = CHECKPOINT_DIR / "base.pt"
torch.save(model.state_dict(), checkpoint_path)

print(f"Checkpoint saved to {checkpoint_path}")
