from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):

    db_url: str = f'postgresql+asyncpg://alfacat187:alfacat@localhost:5432/academy'


settings = Settings()