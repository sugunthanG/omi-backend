from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

clients = []


@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients.remove(websocket)