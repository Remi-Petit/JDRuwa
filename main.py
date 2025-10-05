# main.py
from fastapi import FastAPI
from config.env import get_settings
from routers.health import router as health_router
from routers.auth import router as auth_router
from routers.users import router as users_router

settings = get_settings()

app = FastAPI()

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"name": settings.API_TITLE, "version": settings.API_VERSION}
