from datetime import datetime

from pydantic import BaseModel

from app.db.schemas.pagination import PaginationSchema


class RequestBase(BaseModel):
    message: str


class RequestCreate(RequestBase):
    bottoken: str
    chatid: int


class RequestCreateResponse(RequestBase):
    """ Formatted response for requests before saving to the database """
    author_id: int
    timestamp: datetime = datetime.now()
    telegram_response: str | None = None

    class Config:
        from_attribute = True


class RequestRead(RequestCreateResponse):
    id: int


class PaginatedRequestList(PaginationSchema):
    items: list[RequestRead]



