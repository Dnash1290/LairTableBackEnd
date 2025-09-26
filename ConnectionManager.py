from fastapi import WebSocket
from typing import Dict
import json

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

            self.connections_dict[client_id] = {
                "ws": websocket,
                "client": client_id
            }

            if len(self.connections_dict) == 1:
                self.connections_dict[client_id]["isHost"] = True  
            else:
                self.connections_dict[client_id]["isHost"] = False

            filt = self.connections_dict[client_id].copy()
            filt.pop("ws",None)
            print(filt, "FILT")

            return {
                "success":True, 
                "client":filt,
                "message":f"{client_id} has joined"
                }

        await websocket.close(code=1001, reason=f"{client_id} already has joined in" )
        return {"success":False, "message":f"{client_id} already has joined in"}
        
    def disconnect(self, client_id):
        self.connections_dict.pop(client_id)
        print(self.connections_dict, "fkidps")

    async def echo_all(self, msg):
        disconnected_clients = []
        
        for client in list(self.connections_dict.keys()):
            try:
                if "ws" not in self.connections_dict[client]:
                    disconnected_clients.append(client)
                    continue
                    
                await self.connections_dict[client]["ws"].send_text(json.dumps(msg))
                
            except Exception as e:
                print(f"Failed to send to {client}: {str(e)}")
                disconnected_clients.append(client)
                
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)
        
