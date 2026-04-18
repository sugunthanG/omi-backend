import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.services.alert_service import alert_loop


def create_app():
    app = FastAPI()

    # ✅ CORS FIX (VERY IMPORTANT)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            #"http://localhost:3000",  # frontend (dev)
            "https://omi-frontend-xi.vercel.app/",  # add later (prod)
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ✅ API routes
    app.include_router(api_router, prefix="/api/v1")

    # ✅ Background task (alerts)
    @app.on_event("startup")
    async def start_background_tasks():
        asyncio.create_task(alert_loop())

    return app


app = create_app()