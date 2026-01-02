from fastapi import APIRouter, HTTPException
from app.ml.registry import get_registry

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
def list_models():
    registry = get_registry()
    return registry.list_models()


@router.get("/{model_name}")
def model_info(model_name: str):
    registry = get_registry()
    info = registry.info(model_name)
    if not info:
        raise HTTPException(status_code=404, detail="Model not found")
    return info
