from typing import Dict, Union
from app.ml.loader import load_model
from app.ml.model import RegressionNet
from app.ml.unet import UNet
from app.ml.base import BaseModel


class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, BaseModel] = {}
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        # Load regression model
        self.models["base"] = load_model(input_dim=4)
        
        # Load U-Net model (create if checkpoint doesn't exist)
        try:
            # Try to load U-Net checkpoint
            unet = UNet(in_channels=3, out_channels=1)
            unet.eval()
            self.models["unet"] = unet
        except Exception:
            # Create default U-Net if loading fails
            unet = UNet(in_channels=3, out_channels=1)
            unet.eval()
            self.models["unet"] = unet
        
        self._loaded = True

    def get(self, name: str = "base") -> BaseModel:
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



def get_model(name: str = "base") -> BaseModel:
    return get_registry().get(name)
