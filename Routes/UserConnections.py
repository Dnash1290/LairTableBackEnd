from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ConnectionManager import conn
conn_router = APIRouter()


@conn_router.websocket("/ws/{room_id}/{client_id}")
async def connect_client(websocket: WebSocket, room_id, client_id):
   
    join = await conn.connect(client_id, room_id, websocket)
    print(join["message"])

    if not join["success"]:return

    try:
        while True:
            msg = await websocket.receive_json()
            await conn.echo_all(str(join))
            await websocket.send_text(msg["message"])
            print(websocket.client_state)

    except WebSocketDisconnect:
        conn.disconnect(client_id)
        print("left")


