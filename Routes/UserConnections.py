from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ConnectionManager import conn
conn_router = APIRouter()


@conn_router.websocket("/ws/{room_id}/{client_id}")
async def connect_client(websocket: WebSocket, room_id, client_id):
    try:
        join = await conn.connect(client_id, room_id, websocket)
        await conn.echo_all(join)
        msg = await websocket.receive_json()
        await websocket.send_text(msg["message"])
    
    except WebSocketDisconnect:
        conn.disconnect(client_id)
        print("client disconnected")

