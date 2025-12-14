class DummyModel:

    def predict(self, values: list[float]) -> float:
        return sum(values) / len(values)