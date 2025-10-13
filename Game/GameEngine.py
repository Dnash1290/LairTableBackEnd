from .modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game
import time, asyncio

clients = game.connection.connections_dict

async def investigations():
    try:
        clients = game.investigating()
        db = game.get_all_users()
        for client in clients:
           
            client_info = db[client]
            game.time_stp("investigating", 30)
            print("before info send")
            try:
                await game.connection.echo_all({
                    "action": "game.investigation",
                    "data": {
                        "investigating": client_info
                    }
                })
                print("infor send")
                # Add a short delay between messages
    
                print({
                    "action": "game.investigation",
                    "data": {
                        "investigating": client_info
                    }
                })
                
            except Exception as e:
                print(f"Failed to send message to {client}: {str(e)}")
                
    except Exception as e:
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
    game_status:dict = game.time_stp("game starting",30)
    
    await game.connection.echo_all({
        "action":"game.starting",
        "data":{
            "imposter":imposter,
            "word": game_word,
            "game_status":game_status
            }})

    time.sleep(6)
    await investigations()

    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass