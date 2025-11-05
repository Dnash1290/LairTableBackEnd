from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from Game.MainGame import game
from typing import Dict, List, Type
from Game.GameEngine import *
from Game.modules.UserActivity import *
from pydantic import ValidationError
import asyncio

conn_router = APIRouter()

ACTION_HANDLERS: Dict[str,tuple[Type, callable]]={
    # game ---------------------
    "game.start": (StartAct,game_start),

    #player ------
    "player.info":(PlayerInfo, player_info),
    "player.hint":(PlayerHint, recive_hint),
    "player.vote":(PlayerVote, recive_votes)
}

async def validate_pydantic(websocket, client_id,action_type, msg):
    try:
        Model, handle = ACTION_HANDLERS[action_type]
        data = Model(**msg)
        await handle(websocket, client_id, data) 

    except ValidationError as error:
        payload = {
            "action": "error.log",
            "data":error.errors()
        }

        print(error)
        await game.connection.echo_all(payload)



@conn_router.websocket("/ws/{room_id}/{client_id}")
async def connect_client(websocket: WebSocket, room_id, client_id):
   
    join = await game.connection.connect(client_id, room_id, websocket)
    if not join["success"]:return
    payload = {"action":"player.join","data":join}
    print(game.connection.connections_dict, "################# dict")
    try:
        await game.connection.echo_all(payload)

        while True:
            msg:dict = await websocket.receive_json()
            action_type = msg.get("action")

            if action_type not in ACTION_HANDLERS:
                await websocket.send_json({
                    "action":"invalid action","action_name":action_type
                })

            asyncio.create_task(
                validate_pydantic(websocket, client_id, action_type, msg)
            )   
      
    except WebSocketDisconnect:
        game.connection.disconnect(client_id)
        print(WebSocketDisconnect)
        await game.connection.echo_all({
            "action":"player.left",
            "data":{
                "message":f"player {client_id} has left the game",
                "client":client_id
            }
        })


@conn_router.get("/get_users")
def get_users():
    keys = list(game.connection.connections_dict.keys())
    print("num of users", keys)
    if len(keys) <= 1:
        print(len(keys))
        raise HTTPException(status_code=404, detail="you joined the room 1st")
 
    temp = []

    for user in keys:
        filt = game.connection.connections_dict[user].model_dump()
       
        temp_dic = {}
        temp_dic["message"] = f"{user} has joined"
        temp_dic["client"] =  filt
        temp.append(temp_dic)
 
    return{"clients": temp}

