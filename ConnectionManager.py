from fastapi import WebSocket

class ConnetionManager:
    def __init__(self):
        self.connections_dict: dict[str:WebSocket] = {}
        self.rooms = ["testRoom"]

    async def connect(self, client_id:str, room_id, ebsocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            await websocket.close(code=200, reason=f"{room_id} room is invalid" )
            return f"{room_id} room is invalid"
        
        if client_id not in self.connections_dict:
            self.connections_dict[client_id] = websocket       
            return f"{client_id} has joined"
        
    def disconnect(self, client_id):
        self.connections_dict.pop(client_id)

    async def echo_all(self, msg):
        for client in self.connections_dict.values():
            await client.send_text(msg)

    
conn = ConnetionManager()