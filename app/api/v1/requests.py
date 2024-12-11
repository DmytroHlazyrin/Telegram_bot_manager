from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends

from app.auth.manager import current_user
from app.core.config import settings
from app.db.repositories.requests import RequestsRepository
from app.db.schemas.requests import RequestRead, RequestCreate, \
    RequestCreateResponse, PaginatedRequestList
from app.services.requests import RequestsService
from app.services.telegram import TelegramBotService
from app.db.models import User
from app.utils.pagination import PaginationParams

router = APIRouter()

@router.post("/requests", response_model=RequestCreateResponse, status_code=201)
async def send_massage_endpoint(
        request_data: RequestCreate,
        background_task: BackgroundTasks,
        author: User = Depends(current_user),
):
    author_id = author.id
    response = await TelegramBotService(RequestsRepository).send_message(
        request_data.bottoken,
        request_data.chatid,
        request_data.message,
        author_id,
        background_task
    )
    return response


@router.get("/requests", response_model=PaginatedRequestList)
async def get_messages_endpoint(
        current_user: User = Depends(current_user),
        pagination: PaginationParams = Depends()
):
    """Retrieve a list of messages."""
    return await RequestsService(RequestsRepository).get_requests(current_user, pagination)


