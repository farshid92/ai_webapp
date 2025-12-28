from typing import Dict
from app.ml.loader import load_model
from app.ml.model import RegressionNet
import logging

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Central place to manage multiple models.
    Ready for:
    - ensembles
    - evolutionary selection
    - transfer learning variants
    """

    def __init__(self):
        self.models: Dict[str, RegressionNet] = {}
        

    def get(self, name: str = "base") -> RegressionNet:
        if name not in self.models:
            self.models[name] = load_model()
        return self.models[name]


REGISTRY = ModelRegistry()


def get_model(name: str = "base") -> RegressionNet:
    return REGISTRY.get(name)
