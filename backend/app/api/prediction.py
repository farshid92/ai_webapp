from fastapi import APIRouter
from app.models.schemas import PredictionRequest
from app.ml.registry import get_model
from app.ml.inference import predict

router = APIRouter() 

@router.post("/predict")
def predict_endpoint(request: PredictionRequest):
    model = get_model(request.model_name)
    output = predict(model, request.inputs)

    return {
        "prediction": output
    }