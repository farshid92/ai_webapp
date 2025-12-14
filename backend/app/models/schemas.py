from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    values: List[float]

class PredictionResponse(BaseModel):
    prediction: float