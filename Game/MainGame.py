from ConnectionManager import ConnetionManager
from fastapi import WebSocket
from random import choice


class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:None

    def choose_word():
        return {"category":"disability", "word":"shennoy"}
    
    def choose_imposter(self):
        return {"imposter": choice(self.connection.connections_dict.keys()[0])}
    
    async def start_game(self):
        self.game_status="starting"




game = MainGame()
game.connection = ConnetionManager()