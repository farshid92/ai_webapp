"""
Ensemble Learning API Endpoints

Provides endpoints for ensemble predictions and model comparison.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PredictionRequest
from app.ml.registry import get_registry
from app.ml.ensemble import EnsemblePredictor, ModelComparator
from app.ml.inference import predict
import torch

router = APIRouter(prefix="/ensemble", tags=["ensemble"])


@router.post("/predict")
def ensemble_predict(request: PredictionRequest):
    """
    Make ensemble prediction using multiple models
    
    Args:
        request: Prediction request with inputs and model names
        
    Returns:
        Ensemble prediction result
    """
    try:
        registry = get_registry()
        
        # Get all available models or specified models
        if hasattr(request, 'model_names') and request.model_names:
            model_names = request.model_names
        else:
            model_names = registry.list_models()
        
        # Load models
        models = [registry.get(name) for name in model_names]
        
        if not models:
            raise HTTPException(
                status_code=400,
                detail="No models available for ensemble"
            )
        
        # Create ensemble
        ensemble = EnsemblePredictor(
            models=models,
            method="weighted_average"
        )
        
        # Prepare input
        inputs_tensor = torch.tensor(
            request.inputs,
            dtype=torch.float32
        ).unsqueeze(0)
        
        # Predict
        prediction = ensemble.predict(inputs_tensor)
        
        return {
            "prediction": float(prediction.item()),
            "models_used": model_names,
            "ensemble_size": len(models),
            "method": "weighted_average"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ensemble prediction failed: {str(e)}"
        )


@router.post("/compare")
def compare_models(request: PredictionRequest):
    """
    Compare predictions from multiple models
    
    Args:
        request: Prediction request
        
    Returns:
        Comparison results for all models
    """
    try:
        registry = get_registry()
        model_names = registry.list_models()
        
        models_dict = {name: registry.get(name) for name in model_names}
        comparator = ModelComparator(models_dict)
        
        # Prepare input
        inputs_tensor = torch.tensor(
            request.inputs,
            dtype=torch.float32
        ).unsqueeze(0)
        
        # Compare
        results = comparator.compare_predictions(inputs_tensor)
        
        return {
            "input": request.inputs,
            "comparisons": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model comparison failed: {str(e)}"
        )


@router.post("/predict-with-uncertainty")
def ensemble_predict_with_uncertainty(request: PredictionRequest):
    """
    Make ensemble prediction with uncertainty estimation
    
    Args:
        request: Prediction request
        
    Returns:
        Prediction with uncertainty metrics
    """
    try:
        registry = get_registry()
        model_names = registry.list_models()
        
        models = [registry.get(name) for name in model_names]
        
        if not models:
            raise HTTPException(
                status_code=400,
                detail="No models available"
            )
        
        ensemble = EnsemblePredictor(models=models)
        
        # Prepare input
        inputs_tensor = torch.tensor(
            request.inputs,
            dtype=torch.float32
        ).unsqueeze(0)
        
        # Predict with uncertainty
        result = ensemble.predict_with_uncertainty(inputs_tensor)
        
        return {
            "prediction": float(result["prediction"].item()),
            "uncertainty": float(result["uncertainty"].item()),
            "std": float(result["std"].item()),
            "models_used": model_names
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Uncertainty prediction failed: {str(e)}"
        )


