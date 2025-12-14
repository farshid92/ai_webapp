from fastapi import APIRouter
from app.api.prediction import router as prediction_router

router = APIRouter()

router.include_router(prediction_router, tags=["prediction"])