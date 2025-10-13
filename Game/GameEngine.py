from .modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game
import time, asyncio
import traceback

clients = game.connection.connections_dict
game_start_time = 4
game_investigation_time = 3

async def investigations():
    try:
        round_order = game.investigating()

        for client in round_order:
           
            client_info = clients[client].model_dump()
            game_status = game.time_stp("investigating", game_investigation_time)

            playload = {
                "action": "game.investigation",
                "data": {
                    "investigating": client_info,
                    "game_status": game_status
                }
            }

            try:
                await game.connection.echo_all(playload)
                print(playload)
   
                time.sleep(game_investigation_time)
            except Exception as e:
                print(f"Failed to send message to {client}: {str(e)}")
                
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
    game_status:dict = game.time_stp("game starting",game_start_time)
    
    await game.connection.echo_all({
        "action":"game.starting",
        "data":{
            "imposter":imposter,
            "word": game_word,
            "game_status":game_status
            }})

    print("using sleep ##################")
    time.sleep(game_start_time)
    await investigations()

    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass