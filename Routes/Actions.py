from modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game

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

    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass