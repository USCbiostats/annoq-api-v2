import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DEBUG:bool = os.getenv("DEBUG")
    ES_HOST:str = os.getenv("ES_HOST")
    ES_PORT:int = int(os.getenv("ES_PORT"))
    ES_INDEX:str = os.getenv("ES_INDEX")
    ES_SCHEME:str = os.getenv("ES_SCHEME")
    ES_URL:str = os.getenv("ES_URL")
    FASTAPI_PORT:int = int(os.getenv("FASTAPI_PORT"))
    API_URL: str = str(os.getenv("API_URL"))
    DOWNLOAD_DIR:str = os.getenv("DOWNLOAD_DIR")
    DOWNLOAD_SIZE:int = int(os.getenv("DOWNLOAD_SIZE"))

settings = Settings()
