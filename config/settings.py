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
    ANNOTATION_API:str = os.getenv("ANNOTATION_API")
    FASTAPI_PORT:int = int(os.getenv("FASTAPI_PORT"))

settings = Settings()
