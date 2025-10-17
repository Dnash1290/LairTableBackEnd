
from Game.MainGame import game
from fastapi import WebSocket
import asyncio, traceback
from Game.modules.UserActivity import *
from collections import Counter
import random
from Handler.Player import Player

all_clients = game.connection.connections_dict


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

    if all_clients[client_id].IsHost is False:
        return {
            "action": "error.log",
            "data":{"message":f"{client_id} is not the host to start a match"}
        }

    if len(all_clients) < 3:
        return {
            "action": "error.log",
            "data":{"message": "not enough players to start the game"}
        }
    return



async def recive_hint(ws: WebSocket, client_id, hint:PlayerHint):
    
    if game.current_investigating != client_id:
        await game.connection.echo_all({
            "action":"error.log",
            "message":f"{client_id} is not been currently investgating"
        })
        return
    
    print("data recived" ,game.current_investigating, client_id)
    global hint_data
    hint_data = hint.model_dump()
    game.remaining_players[client_id].words.append(hint.data.word)
    hint_event.set()


# investigating round order
def investigating_list():
    clients_ids = list(game.remaining_players.keys())
    random.shuffle(clients_ids)
    chance = random.randint(1,1000)
    

    #checks if imposter 1 in the list then list re suffled, there is 1000/1 chance its not
    if clients_ids[0] != game.imposter:return clients_ids
    if chance != 69: 
        num = random.randint(1,len(clients_ids)-1)
        print("num", num)
        temp = clients_ids[num]
        clients_ids[num] = clients_ids[0]
        clients_ids[0] = temp 
        return clients_ids

    print("\n\n\n\n --------------UN LUCKY IMPOSTER--------------")
    return clients_ids


async def investigations():
    try:
        round_order = investigating_list()
        for client in round_order:
            
            game.current_investigating = client
            client_info = game.remaining_players[client].model_dump()
            game_status = game.time_stp("game.investigating", investigation_time)

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
                print(f"TIME IS UPPP {client}: {str(e)}")
                print("maybe asyncio failed idk")

        print("end")
    except Exception as e:
        traceback.print_exc()
        print(f"Investigation failed: {str(e)}")
        # Clean up any invalid connections


def vote_results(count:dict):
    voted_client = ""
    votes = 0
    
    for key in count.keys():
        if count[key] < votes:
            continue
        votes = count[key]
        voted_client = key

    if game.imposter != voted_client: 

        return [{"voted_client":voted_client}, {"is_imposter":False}]
    
    return [{"voted_client":voted_client},{"is_imposter":True}]


async def recive_votes(ws: WebSocket, client_id:str, player:PlayerVote):
    player_vote = player.data.vote

    try:
        if game.game_status["status"] != "game.voting" :
            print("game is not started yet")
            return
    except:
        pass

    vote_name = player_vote
    
    if vote_name not in game.remaining_players and client_id not in game.remaining_players:
        print("vote invalid sinces user not found")
        return

    #if user already voted, then then the new vote is overwritten
    if game.remaining_players[client_id].voted_name is not None: 
        old_vote = game.remaining_players[client_id].voted_name
        game.remaining_players[client_id].voted_name = player_vote 

        try:
            index = game.votes.index(old_vote)
            game.votes[index] = player_vote
            print(f"{old_vote} is been overwritten by {player_vote}")
        except ValueError as e :
            print(e)
        
        return

    game.votes.append(vote_name)
    game.remaining_players[client_id].voted_name = player_vote
   
    await game.connection.echo_all({
        "action": "player.vote",
        "data":{
            "vote":vote_name 
        }
    })

async def voting():
    game_status = game.time_stp("game.voting",voting_time)
    await game.connection.echo_all({
        "action": "game.voting",
        "data":{
            "message":"start voting..",
            "game_status":game_status
        }
    })
    await asyncio.sleep(voting_time)
    count = Counter(game.votes)

    voted_client = vote_results(count)
    print("voting completed", game.votes, "most voted client", voted_client)

    try:
        game.remaining_players.pop(voted_client[0]["voted_client"])
    except TypeError as e:
        print(e)
        print("might be a draw ngl")

    await game.connection.echo_all({
        "action": "game.vote_results",
        "data":{ 
            "vote":count,
            **voted_client[0],
            **voted_client[1]
        }
    })


