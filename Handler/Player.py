from pydantic import BaseModel, PrivateAttr
from typing import Dict, Optional
from fastapi import WebSocket

class Player(BaseModel):
    username: str
    IsHost: bool = False
    words: Optional[list[str]] = []
    __ws:Optional[WebSocket] = PrivateAttr(default=None)





