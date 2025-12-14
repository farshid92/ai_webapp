from fastapi import APIRouter
from app.models.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter()
service = PredictionService()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    prediction = service.predict(request.values)
    return PredictionResponse(prediction=prediction)