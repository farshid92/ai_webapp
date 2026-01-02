from abc import ABC, abstractmethod
import torch

class BaseModel(ABC):
    """
    Unified interface for all ML models
    """

    @abstractmethod
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        pass