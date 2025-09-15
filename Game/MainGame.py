from ConnectionManager import ConnetionManager
from fastapi import WebSocket
import random


class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:None

    def choose_word(self):
        return {"category":"disability", "word":"shennoy"}
    
    def choose_imposter(self):
        imposter = random.choice(list(self.connection.connections_dict.keys())[0])
        return {"imposter": imposter}
    
    def start_game(self):
        self.game_status="starting"




game = MainGame()
game.connection = ConnetionManager()