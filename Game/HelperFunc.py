
from Game.MainGame import game
from fastapi import WebSocket
import asyncio, traceback
from Game.modules.UserActivity import *

clients = game.connection.connections_dict
investigation_time = 20
voting_time = 30

hint_data = None
hint_event = asyncio.Event()


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



async def recive_hint(ws: WebSocket, client_id, hint:PlayerHint):
    print("data recived" ,game.current_investigating, client_id)

    if game.current_investigating != client_id:
        await game.connection.echo_all({
            "action":"error.log",
            "message":f"{client_id} is not been currently investgating"
        })
        return
    
    global hint_data
    hint_data = hint.model_dump()
    clients[client_id].words.append(hint.data.word)
    hint_event.set()



async def investigations():
    try:
        round_order = game.investigating_list()
        
        for client in round_order:
            
            game.current_investigating = client
            client_info = clients[client].model_dump()
            game_status = game.time_stp("investigating", investigation_time)

            playload = {
                "action": "game.investigation",
                "data": {
                    "investigating": client_info,
                    "game_status": game_status
                }
            }

            try:
                await game.connection.echo_all(playload)
                #recieve_task = asyncio.create_task(hint_event)
                await asyncio.wait_for(hint_event.wait(),
                    timeout=investigation_time
                )
               
                hint_event.clear()
                await game.connection.echo_all(hint_data)

            except asyncio.TimeoutError as e:
                
                await game.connection.echo_all({
                    "action": "player.hint",
                    "data":{
                        "hint": None
                    }
                })
                print(f"Failed to send message to {client}: {str(e)}")
                print("maybe asyncio failed idk")

        print("end")
    except Exception as e:
        traceback.print_exc()
        print(f"Investigation failed: {str(e)}")
        # Clean up any invalid connections

async def recive_votes(ws: WebSocket, client_id:str, player:PlayerVote):
    vote = player.data.vote
    if vote not in clients:
        print("vote invalid sinces user not found")
        return
    
    game.votes.append(vote)
    clients[client_id].votes.append(vote)
    

async def voting():
    game_status = game.time_stp("voting",voting_time)
    await game.connection.echo_all({
        "action": "game.voting",
        "data":{
            "message":"start voting..",
            "game_status":game_status
        }
    })
    await asyncio.sleep(voting_time)


