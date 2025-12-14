from app.models.dummy_model import DummyModel

class PredictionService:
    def __init__(self):
        self.model = DummyModel()

    def predict(self, values: list[float]) -> float:
        return self.model.predict(values)