from app.models.schemas import PredictRequest, PredictResponse
from app.ml.registry import get_model
from app.ml.inference import predict

@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(req: PredictRequest):
    model = get_model()
    result = predict(model, req.inputs)
    return PredictResponse(result=result)
backend/app/models