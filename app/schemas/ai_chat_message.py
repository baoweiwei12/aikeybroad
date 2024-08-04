import enum
from typing import List, Literal, TypedDict
from pydantic import BaseModel



class AiChatMessage(BaseModel):
    id: int
    user_id: int
    role: str
    content: str


    class Config:
        from_attributes = True

class AiChatMessageCreate(BaseModel):
    user_id: int
    role: str
    content: str

