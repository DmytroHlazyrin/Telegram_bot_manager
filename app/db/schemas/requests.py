from datetime import datetime

from pydantic import BaseModel

from app.db.schemas.pagination import PaginationSchema


class RequestBase(BaseModel):
    message: str


class RequestCreate(RequestBase):
    bottoken: str
    chatid: int


class RequestCreateResponse(BaseModel):
    telegram_response: dict

    class Config:
        arbitrary_types_allowed = True


class RequestRead(RequestCreateResponse):
    id: int
    author_id: int
    timestamp: datetime = datetime.now()
    bot_token: str
    chat_id: int


class PaginatedRequestList(PaginationSchema):
    items: list[RequestRead]
