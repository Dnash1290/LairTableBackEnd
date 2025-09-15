from fastapi import WebSocket
from typing import Dict

class ConnetionManager:
    def __init__(self):
        self.connections_dict: Dict = {}
        self.rooms = ["testRoom"]

    async def connect(self, client_id:str, room_id,websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            await websocket.close(code=1001, reason=f"{room_id} room is invalid" )
            return {"success":False, "message":f"{room_id} room is invalid"}
        
        if client_id not in self.connections_dict:
            self.connections_dict[client_id] = websocket       
            return {"success":True, "message":f"{client_id} has joined"}

        await websocket.close(code=1001, reason=f"{client_id} already has joined in" )
        return {"success":False, "message":f"{client_id} already has joined in"}
        
    def disconnect(self, client_id):
        self.connections_dict.pop(client_id)
        print(self.connections_dict, "fkidps")

    async def echo_all(self, msg):
        for client in self.connections_dict.values():
            await client.send_text(str(msg))

    
