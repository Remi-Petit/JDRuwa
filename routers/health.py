# routers/health.py
import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.connect import check_db

router = APIRouter(tags=["health"])

@router.get("/health/db")
async def health_db():
    start = time.perf_counter()
    try:
        info = await check_db()
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        info["latency_ms"] = latency_ms
        return info
    except Exception as e:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Erreur interne pendant le contrôle de santé de la base de données.",
                "details": str(e),
                "latency_ms": latency_ms,
            },
        )

@router.get("/health")
async def health():
    return {"status": "ok"}
