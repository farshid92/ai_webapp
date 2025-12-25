import torch
from app.ml.model import RegressionNet
from pathlib import Path

# Resolve project root: /app/app
ROOT = Path(__file__).resolve().parents[2]

CHECKPOINT_DIR = ROOT / "ml" / "checkpoints"
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

model = RegressionNet(input_dim=3)

checkpoint_path = CHECKPOINT_DIR / "base.pt"
torch.save(model.state_dict(), checkpoint_path)

print(f"Checkpoint saved to {checkpoint_path}")
