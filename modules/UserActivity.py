from pydantic import BaseModel
from typing import Literal, Dict

class ChatAct(BaseModel):
    action: Literal["player.chat"]
    message:str


class StartAct(BaseModel):
    action: Literal["game.start"]
    