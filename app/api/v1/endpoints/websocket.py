from fastapi import APIRouter, WebSocket
from app.core.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    print("🔥 WebSocket HIT")   # 👈 ADD THIS

    await manager.connect(websocket)

    print("✅ Connected")       # 👈 ADD THIS

    try:
        while True:
            await websocket.receive_text()
    except:
        print("❌ Disconnected")
        manager.disconnect(websocket)