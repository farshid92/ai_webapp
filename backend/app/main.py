from fastapi import FastAPI
from app.api import prediction

app = FastAPI()

app.include_router(
    prediction.router,
    prefix="/api",
    tags=["prediction"]
)

@app.get("/health")
def health():
    return {"status": "ok"}
