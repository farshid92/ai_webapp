import torch
import torch.nn as nn

class RegressionNet(nn.Module):
    """
    Minimal but extensible network.
    This is a placeholder for:
    - transfer learning
    - ensemble usage
    - GA-optimized architectures
    """

    def __init__(self, input_dim: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
