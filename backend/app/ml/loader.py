import torch
from pathlib import Path
from app.ml.model import RegressionNet

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# default checkpoint directory - relative to this file
# loader.py is in app/ml/, so parents[1] is app/, parents[0] is app/ml/
CHECKPOINT_DIR = Path(__file__).resolve().parent / "checkpoints"


def load_model(
    checkpoint_name: str = "base.pt",
    input_dim: int = 4,
) -> RegressionNet:
    checkpoint_path = CHECKPOINT_DIR / checkpoint_name
    
    # Try to load model, but if file doesn't exist or is empty, use untrained model
    if checkpoint_path.exists() and checkpoint_path.stat().st_size > 0:
        try:
            # Try to infer input_dim from saved state dict
            state_dict = torch.load(checkpoint_path, map_location=DEVICE)
            if 'net.0.weight' in state_dict:
                # First layer weight shape is (out_features, in_features)
                saved_input_dim = state_dict['net.0.weight'].shape[1]
                if saved_input_dim != input_dim:
                    print(f"Note: Saved model has input_dim={saved_input_dim}, but requested {input_dim}. Using saved dimension.")
                    input_dim = saved_input_dim
        except Exception as e:
            print(f"Warning: Could not read model dimensions from {checkpoint_path}: {e}. Using default input_dim={input_dim}.")
    
    model = RegressionNet(input_dim=input_dim)
    
    # Try to load the state dict
    if checkpoint_path.exists() and checkpoint_path.stat().st_size > 0:
        try:
            model.load_state_dict(
                torch.load(checkpoint_path, map_location=DEVICE)
            )
        except Exception as e:
            print(f"Warning: Could not load model from {checkpoint_path}: {e}. Using untrained model.")
    else:
        print(f"Warning: Model checkpoint not found or empty at {checkpoint_path}. Using untrained model.")
    
    model.to(DEVICE)
    model.eval()

    return model
