from fastapi import APIRouter
from app.api.prediction import router as prediction_router
from app.api.health import router as health_router
from app.api.models import router as models_router
from app.api.segmentation import router as segmentation_router
from app.api.ensemble import router as ensemble_router
from app.api.optimization import router as optimization_router

router = APIRouter()

router.include_router(health_router)
router.include_router(prediction_router, prefix="/api")
router.include_router(models_router, prefix="/api")
router.include_router(segmentation_router, prefix="/api")
router.include_router(ensemble_router, prefix="/api")
router.include_router(optimization_router, prefix="/api")
