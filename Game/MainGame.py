from ConnectionManager import ConnetionManager
from fastapi import WebSocket
import random
from datetime import datetime, timedelta, timezone


class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:dict = {}

    def choose_word(self):
        return {"category":"disability", "word":"shennoy"}
    
    def choose_imposter(self):
        return random.choice(list(self.connection.connections_dict.keys()))
        
    def time_stp(self, stp_name, duration_sec):
        self.game_status["status"]= stp_name
        time = (datetime.now(timezone.utc) + timedelta(seconds=duration_sec)).timestamp()
        self.game_status["end_time"] = round(time,3)
        return self.game_status



game = MainGame()
game.connection = ConnetionManager()