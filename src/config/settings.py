import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    DEBUG:bool = os.getenv("DEBUG")
    ES_HOST:str = os.getenv("ES_HOST")
    ES_PORT:int = int(os.getenv("ES_PORT"))
    ES_INDEX:str = os.getenv("ES_INDEX")
    ES_URL:str = os.getenv("ES_URL")
    SITE_HOST:str = os.getenv("SITE_HOST")
    SITE_PORT:int = int(os.getenv("SITE_PORT"))
    SITE_URL: str = str(os.getenv("SITE_URL"))
    SITE_DOWNLOAD_DIR:str = os.getenv("SITE_DOWNLOAD_DIR")
    SIZE_DOWNLOAD_SIZE:int = int(os.getenv("SIZE_DOWNLOAD_SIZE"))
    GA_MEASUREMENT_ID:str = os.getenv("GA_MEASUREMENT_ID", "")
    GA_API_SECRET:str = os.getenv("GA_API_SECRET", "")
settings = Settings()
