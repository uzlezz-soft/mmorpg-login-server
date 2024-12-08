from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./temp.db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'CHANGE_IN_DOT_ENV0')
    REFRESH_SECRET_KEY: str = os.getenv('REFRESH_SECRET_KEY', 'CHANGE_IN_DOT_ENV1')
    SESSION_SECRET_KEY: str = os.getenv('SESSION_SECRET_KEY', 'CHANGE_IN_DOT_ENV2')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')

    JWT_TIMEOUT_MINUTES: int = os.getenv('JWT_TIMEOUT_MINUTES', 30)
    JWT_REFRESH_TIMEOUT_MINUTES: int = os.getenv('JWT_REFRESH_TIMEOUT_MINUTES', 60 * 24 * 7)
    SESSION_TIMEOUT_MINUTES: int = os.getenv('SESSION_TIMEOUT_MINUTES', 60 * 24)

    SERVER_HEARTBEAT_TIMEOUT_SECONDS: int = os.getenv('SERVER_HEARTBEAT_TIMEOUT_SECONDS', 60)
    SERVER_TRUSTED_IPS: list = os.getenv('SERVER_TRUSTED_IPS', ["127.0.0.1"])
    USER_JOIN_REQUEST_TIMEOUT_SECONDS: int = os.getenv('USER_JOIN_REQUEST_TIMEOUT_SECONDS', 30)

settings = Settings()