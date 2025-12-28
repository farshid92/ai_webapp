from fastapi import APIRouter
from app.api.prediction import router as prediction_router
from app.api.health import router as health_router

router = APIRouter()

router.include_router(prediction_router, tags=["prediction"])
router.include_router(health_router)