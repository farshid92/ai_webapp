from fastapi import APIRouter, HTTPException
from app.models.schemas import PredictionRequest
from app.ml.registry import get_model
from app.ml.inference import predict

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post("/")
def predict_endpoint(request: PredictionRequest):
    try:
        model = get_model(request.model_name)
        output = predict(model, request.inputs)

        return {
            "prediction": output,
            "model": request.model_name
        }
    except ValueError as e:
        # Dimension mismatch or validation errors
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Model not available: {str(e)}. Please ensure model files are present."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
