from modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game

async def game_start(ws:WebSocket, client_id:str, data):
    print(data.data,"OBJECT")
    if data.data.get("player_type", "OBJECT") != "host":
        return
    
    game.connection.echo_all({
            "action":"game.status",
            "data":{
                "message":"game is starting"
            }})
    
    game.start_game()
    imposter:str = game.choose_imposter()
    game_word:dict = game.choose_word()

    
    await game.connection.echo_all({
        "action":"game.imposter",
        "data":{
            "imposter": imposter
            }})

    await game.connection.echo_all({
        "action":"game.word",
        "data":{
            "choice":game_word
        }})
    
async def player_info(ws:WebSocket, client_id:str, data:dict):
    pass