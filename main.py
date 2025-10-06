# main.py
from fastapi import FastAPI, HTTPException
from config.env import get_settings
from routers import health, auth, users, roles, permissions
import models # From models/__init__.py to ensure models are registered

settings = get_settings()
app = FastAPI()

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router )
app.include_router(permissions.router)

@app.get("/")
async def root():
    return {"name": settings.API_TITLE, "version": settings.API_VERSION}

