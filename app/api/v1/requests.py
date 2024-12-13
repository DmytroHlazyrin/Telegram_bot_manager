from fastapi import APIRouter, BackgroundTasks, Depends

from app.auth.manager import current_user
from app.db.repositories.requests import RequestsRepository
from app.db.schemas.requests import RequestCreate, \
    RequestCreateResponse, PaginatedRequestList
from app.services.requests import RequestsService
from app.services.telegram import TelegramBotService
from app.db.models import User
from app.utils.pagination import PaginationParams

router = APIRouter()

@router.post("/requests",
             response_model=RequestCreateResponse,
             status_code=201)
async def send_request_endpoint(
        request_data: RequestCreate,
        background_task: BackgroundTasks,
        author: User = Depends(current_user),
) -> RequestCreateResponse:
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
async def get_request_endpoint(
        current_user: User = Depends(current_user),
        pagination: PaginationParams = Depends()
) -> PaginatedRequestList:
    """Retrieve a list of messages."""
    return await RequestsService(RequestsRepository).get_requests(
        current_user, pagination)

@router.get("/users/{user_id}/requests",
            response_model=PaginatedRequestList)
async def get_user_requests_endpoint(
        user_id: int,
        current_user: User = Depends(current_user),
        pagination: PaginationParams = Depends()
) -> PaginatedRequestList:
    """Retrieve a list of messages for a specific user."""
    return await RequestsService(RequestsRepository).get_user_requests(
        current_user, user_id, pagination)
