from Handler.Connections import ConnetionManager
from fastapi import WebSocket
import random
from datetime import datetime, timedelta, timezone
from Handler.Player import Player

# need to focus on when user disconnects? like what happenes to the round

class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:dict = {}
        self.imposter :str
        self.current_investigating: str = ""
        self.word: str
        self.category:str
        self.votes: list = []
        self.remaining_players:dict[str, Player] = {}
        

    def get_all_users(self):
        print("------- Original connections ------")
        pass

    def choose_word(self):
        self.category, self.word = "disabilty", "shennoy"
        return {"category":"disability", "word":"shennoy", "words":["there will be a list of words here"]}
    
    def choose_imposter(self):
        self.imposter = random.choice(list(self.connection.connections_dict.keys()))
        return self.imposter
    
    def time_stp(self, stp_name, duration_sec):
        self.game_status["status"]= stp_name
        time = (datetime.now(timezone.utc) + timedelta(seconds=duration_sec)).timestamp()
        self.game_status["end_time"] = round(time,3)
        return self.game_status






game = MainGame()
game.connection = ConnetionManager()
#game.imposter = "user 1"
#game.connection.connections_dict = {
#    "user 1":{"ws":"websocket","client":"name 1"},
#    "user 2":{"ws":"websocket","client":"name 2"},
#    "user 3":{"ws":"websocket","client":"name 3"},
#    "user 4":{"ws":"websocket","client":"name 4"}}

#print(game.get_all_users())

#print(game.investigating())