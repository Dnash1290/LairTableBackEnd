from pydantic import BaseModel
from typing import Literal, Dict

class ChatAct(BaseModel):
    action: Literal["player.chat"]
    data:dict


class StartAct(BaseModel):
    action: Literal["game.start"]
    data:dict
    
class PlayerInfo(BaseModel):
    action:Literal["player.info"]
    data:dict