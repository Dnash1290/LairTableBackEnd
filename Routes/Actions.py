from modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game
import time, asyncio

async def investigations():
    try:
        clients = game.investigating()
        db = game.get_all_users()
        for client in clients:
            # Check if client still exists and has valid websocket
            if client not in game.connection.connections_dict or "ws" not in game.connection.connections_dict[client]:
                print(f"Client {client} connection invalid")
                continue
                
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
                time.sleep(7)
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
        for client_id in list(game.connection.connections_dict.keys()):
            if "ws" not in game.connection.connections_dict[client_id]:
                game.connection.disconnect(client_id)

        

async def game_start(ws:WebSocket, client_id:str, data):
    print(data.data,"OBJECT")
    if data.data.get("player_type") != "host":
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

    #time.sleep(30)
    await investigations()

    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass