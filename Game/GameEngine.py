from Game.modules.UserActivity import *
from fastapi import WebSocket
from Game.MainGame import game
import time, asyncio
import traceback

clients = game.connection.connections_dict
start_time = 4
investigation_time = 20
hint_data = None
hint_event = asyncio.Event()

async def recive_hint(ws: WebSocket, client_id, data:PlayerHint):
    print("data recived" ,data)
    global hint_data
    hint_data = data.model_dump()
    hint_event.set()

async def investigations():
    try:
        round_order = game.investigating()

        for client in round_order:
           
            client_info = clients[client].model_dump()
            game_status = game.time_stp("investigating", investigation_time)

            playload = {
                "action": "game.investigation",
                "data": {
                    "investigating": client_info,
                    "game_status": game_status
                }
            }

            try:
                await game.connection.echo_all(playload)
                #recieve_task = asyncio.create_task(hint_event)
                await asyncio.wait_for(hint_event.wait(),
                    timeout=investigation_time
                )
               
                hint_event.clear()
                await game.connection.echo_all(hint_data)

            except asyncio.TimeoutError as e:
                
                await game.connection.echo_all({
                    "action": "player.hint",
                    "data":{
                        "hint": None
                    }
                })
                print(f"Failed to send message to {client}: {str(e)}")
                print("maybe asyncio failed idk")

        print("end")
    except Exception as e:
        traceback.print_exc()
        print(f"Investigation failed: {str(e)}")
        # Clean up any invalid connections
    

        

async def game_start(ws:WebSocket, client_id:str, data):

    if clients[client_id].IsHost is False:
        await ws.send_json({
            "action": "error.log",
            "data":{"message":f"{client_id} is not the host to start a match"}
        })
        return

    if len(clients) < 3:
        await ws.send_json({
            "action": "error.log",
            "data":{"message": "not enough players to start the game"}
        })
        return

    imposter:str = game.choose_imposter()
    game_word:dict = game.choose_word()
    game_status:dict = game.time_stp("game starting",start_time)
    
    await game.connection.echo_all({
        "action":"game.starting",
        "data":{
            "imposter":imposter,
            "word": game_word,
            "game_status":game_status
            }})

    print("using sleep ##################")
    await asyncio.sleep(start_time)
    asyncio.create_task(investigations())

    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass


