from pydantic import BaseModel, PrivateAttr
from typing import Dict, Optional
from fastapi import WebSocket

class Player(BaseModel):
    username: str
    IsHost: bool = False
    words: list[str] = []
    votes:list[str] = []
    __ws:Optional[WebSocket] = PrivateAttr(default=None)

    @property
    def ws(self) -> WebSocket: 
        return self.__ws

    @ws.setter
    def ws(self, ws: WebSocket):
        self.__ws = ws



