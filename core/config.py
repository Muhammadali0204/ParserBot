from aiogram import Bot
from pydantic_settings import BaseSettings
from aiogram.client.default import DefaultBotProperties

from core.types import MainData


class Settings(BaseSettings):
    CHAT_ID: int
    BOT_TOKEN: str
    PASSWORD: str
    USERNAME: str
    BASE_URL: str
    
    class Config:
        env_file = '.env'
        
settings = Settings()


DATA: MainData = {
    "session": None,
    "data": None
}

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
