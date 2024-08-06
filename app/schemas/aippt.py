from datetime import datetime
from pydantic import BaseModel



class AiPPTRecordCreate(BaseModel):
    user_id: int
    text: str
    sid: str
    cover_img_src: str
    title: str
    sub_title: str
    process: int | None = None
    ppt_url: str | None = None
    err_msg: str | None = None
    error_count: int  = 0

class AiPPTRecordUpdate(BaseModel):
    process: int | None = None
    ppt_url: str | None = None
    err_msg: str | None = None
    error_count: int  | None = None

class AiPPTRecord(AiPPTRecordCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True