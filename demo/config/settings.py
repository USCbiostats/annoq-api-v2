import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Settings(BaseSettings):
    SITE_API_URL:str = os.getenv("SITE_URL")

settings = Settings()
