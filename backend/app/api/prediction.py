from fastapi import APIRouter
from app.models.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter() 
service = PredictionService()

@router.post("/predict")
def predict(request: PredictionRequest):
    inputs = request.inputs
    model_name = request.model_name

    prediction = service.predict(inputs, model_name)

    return {
        "prediction": prediction,
        "model": model_name
    }