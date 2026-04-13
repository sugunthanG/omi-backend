from fastapi import APIRouter
from app.api.v1.endpoints import health, protected, user, trading
from app.api.v1.endpoints import websocket


api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(protected.router, prefix="/protected", tags=["Protected"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(trading.router, prefix="/trading", tags=["Trading"])
api_router.include_router(websocket.router)