from pydantic import BaseModel
from typing import List, Optional

class PredictionRequest(BaseModel):
    inputs: List[float]
    model_name: Optional[str] = "base"


class PredictionResponse(BaseModel):
    result: float