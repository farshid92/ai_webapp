from typing import List
from app.models.dummy_model import DummyModel


class PredictionService:
    def __init__(self):
        self.models = {
            "base": DummyModel()
        }

    def predict(self, inputs: List[float], model_name: str) -> float:
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found")

        model = self.models[model_name]
        return model.predict(inputs)
