from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from Game.MainGame import game
conn_router = APIRouter()


@conn_router.websocket("/ws/{room_id}/{client_id}")
async def connect_client(websocket: WebSocket, room_id, client_id):
   
    join = await game.connection.connect(client_id, room_id, websocket)
    if not join["success"]:return
    payload = {"action":"log","data":join}

    try:
        while True:
            msg = await websocket.receive_json()
            await game.connection.echo_all(str(payload))
         

    except WebSocketDisconnect:
        game.connection.disconnect(client_id)
        await game.connection.echo_all(str({
            "action":"log",
            "data":{
                "message":f"player {client_id} has left the game",
                "client_id":client_id
            }
        }))


