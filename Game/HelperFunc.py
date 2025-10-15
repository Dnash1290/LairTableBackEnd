
from Game.MainGame import game
clients = game.connection.connections_dict

def validate_start(client_id:str):
    if "status" in game.game_status:
        return{
            "action": "error.log",
            "data": {"message": "game is already in progess"}
        }

    if clients[client_id].IsHost is False:
        return {
            "action": "error.log",
            "data":{"message":f"{client_id} is not the host to start a match"}
        }

    if len(clients) < 3:
        return {
            "action": "error.log",
            "data":{"message": "not enough players to start the game"}
        }
    return

