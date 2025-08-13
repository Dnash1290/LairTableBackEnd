from pydantic import BaseModel
from typing import Literal

class ChatAct(BaseModel):
    action: Literal["chat"]
    message:str
    