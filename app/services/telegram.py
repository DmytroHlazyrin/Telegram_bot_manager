from datetime import datetime

from fastapi import BackgroundTasks, HTTPException
from telegram import Bot
from telegram.error import TelegramError, InvalidToken


from app.utils.repository import AbstractRepository


class TelegramBotService:
    def __init__(self, requests_repo: AbstractRepository):
        self.bot = Bot
        self.requests_repo = requests_repo()

    async def send_message(
            self,
            token: str,
            chat_id: int,
            text: str,
            author_id: int,
            background_tasks: BackgroundTasks
    ):
        log_data = {
            "bot_token": token,
            "chat_id": chat_id,
            "message": text,
            "author_id": author_id,
            "timestamp": datetime.now(),
        }

        try:
            response = await self.bot(token=token).send_message(chat_id=chat_id, text=text)
            log_data["telegram_response"] = response.to_dict()

        except InvalidToken:
            raise HTTPException(status_code=401, detail=f"Failed to send message to Telegram. Error: Invalid token")

        except TelegramError as e:
            raise HTTPException(status_code=404, detail=f"Failed to send message to Telegram. Error: {e}")

        # Write to logs asynchronously to avoid blocking the request
        finally:
            background_tasks.add_task(self.requests_repo.add_one, log_data)

        return {"telegram_response": log_data["telegram_response"]}
