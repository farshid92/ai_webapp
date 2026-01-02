from typing import Dict
from app.ml.loader import load_model
from app.ml.model import RegressionNet


class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, RegressionNet] = {}
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        # Load model with default input_dim=4 to match common use case
        # The model will work with any input_dim, but we need to match saved checkpoint
        self.models["base"] = load_model(input_dim=4)
        self._loaded = True

    def get(self, name: str = "base") -> RegressionNet:
        if not self._loaded:
            self.load()
        if name not in self.models:
            raise KeyError(f"Model '{name}' not found")
        return self.models[name]

    def list_models(self):
        if not self._loaded:
            self.load()
        return list(self.models.keys())

    def info(self, name: str):
        if not self._loaded:
            self.load()
        if name not in self.models:
            return None
        return {
            "name": name,
            "version": "0.1",
            "type": self.models[name].__class__.__name__,
        }



REGISTRY: ModelRegistry | None = None

def get_registry() -> ModelRegistry:
    global REGISTRY
    if REGISTRY is None:
        REGISTRY = ModelRegistry()
    return REGISTRY



def get_model(name: str = "base") -> RegressionNet:
    return get_registry().get(name)
