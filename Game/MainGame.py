from Handler.Connections import ConnetionManager
from fastapi import WebSocket
import random
from datetime import datetime, timedelta, timezone

class MainGame:
    def __init__(self):
        self.connection: ConnetionManager
        self.chat: None
        self.game_status:dict = {}
        self.imposter :str
        self.current_investigating: str
        self.word: str
        self.category:str

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

# investigating round order
    def investigating_list(self):
        clients_ids = list(self.connection.connections_dict.keys())
        random.shuffle(clients_ids)
        chance = random.randint(1,1000)
        

        #checks if imposter 1 in the list then list re suffled, there is 1000/1 chance its not
        if clients_ids[0] != self.imposter:return clients_ids
        if chance != 69: 
            num = random.randint(1,len(clients_ids)-1)
            print("num", num)
            temp = clients_ids[num]
            clients_ids[num] = clients_ids[0]
            clients_ids[0] = temp 
            return clients_ids

        print("\n\n\n\n --------------UN LUCKY IMPOSTER--------------")
        return clients_ids




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