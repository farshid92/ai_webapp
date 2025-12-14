from fastapi import FastAPI
from app.api.router import router

app = FastAPI(
    title="AI WebApp Backend",
    version="0.1.0",
    description="Backend API for AI Web Application"
)

app.include_router(router, prefix="/api")

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}