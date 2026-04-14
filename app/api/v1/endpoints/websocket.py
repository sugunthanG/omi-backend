from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("✅ Client connected")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("❌ Client disconnected")