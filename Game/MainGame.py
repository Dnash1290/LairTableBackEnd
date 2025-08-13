from ConnectionManager import ConnetionManager
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
        


game = MainGame()
game.connection = ConnetionManager()