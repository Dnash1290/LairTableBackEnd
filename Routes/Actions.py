from modules import UserActivity
from fastapi import WebSocket
from Game.MainGame import game

def game_start(ws, client_id:str, data:dict):
    if data.get("data",{}).get("player_type") != "host":
        return
    
    game.game_status = "starting"
    