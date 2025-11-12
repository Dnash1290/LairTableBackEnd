from Game.modules.UserActivity import *
from fastapi import WebSocket
from Game.MainGame import game
import asyncio
from Game.HelperFunc import *

clients = game.connection.connections_dict
start_time = 4

async def game_start(ws:WebSocket, client_id:str, data):
    
    game.remaining_players = clients.copy()
    
    if validate_start(client_id):
        await game.connection.echo_all(validate_start(client_id))
        return

    imposter:str = game.choose_imposter()
    game_word:dict = game.choose_word()
    game_status:dict = game.time_stp("game.starting",start_time)
   
    await game.connection.echo_all({
        "action":"game.starting",
        "data":{
            "imposter":imposter,
            "word": game_word,
            "game_status":game_status
            }})

    await asyncio.sleep(start_time)
    print("start investigating....############################")
    await investigations()
    print("start voting")
    await voting()
    print(len(game.remaining_players))
    
    #reset game status soo nest round can be started
    game.game_status = {}


    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass


