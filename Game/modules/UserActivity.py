from pydantic import BaseModel
from typing import Literal, Dict, Any

class ChatAct(BaseModel):
    action: Literal["player.chat"]
    data:dict

class StartAct(BaseModel):
    action: Literal["game.start"]
    data:dict
    
class PlayerInfo(BaseModel):
    action:Literal["player.info"]
    data:dict

class Word(BaseModel):word: str

class PlayerHint(BaseModel):
    action: Literal["player.hint"]
    data: Word

class Vote(BaseModel): vote: str

class PlayerVote(BaseModel):
    action: Literal["player.vote"]
    data: Vote