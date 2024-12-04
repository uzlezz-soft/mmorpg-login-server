from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./temp.db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'CHANGE_IN_DOT_ENV')
    REFRESH_SECRET_KEY: str = os.getenv('REFRESH_SECRET_KEY', 'CHANGE_IN_DOT_ENV')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')

    JWT_TIMEOUT_MINUTES: int = os.getenv('JWT_TIMEOUT_MINUTES', 30)
    JWT_REFRESH_TIMEOUT_MINUTES: int = os.getenv('JWT_REFRESH_TIMEOUT_MINUTES', 60 * 24 * 7)

settings = Settings()