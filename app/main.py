import asyncio
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.services.alert_service import alert_loop


def create_app():
    app = FastAPI()

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def start_background_tasks():
        asyncio.create_task(alert_loop())

    return app


app = create_app()