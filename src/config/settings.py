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
    # Describe the ES_INDEX data, returned by /version: its genome build (e.g.
    # GRCh37/hg19), the dbSNP build of its rsIDs (e.g. 151) and the WGSA version
    # it was annotated with. None (null in /version) when the deployment's .env
    # does not set them.
    ANNOQ_GENOME_BUILD:str | None = os.getenv("ANNOQ_GENOME_BUILD")
    ANNOQ_DBSNP_RELEASE:str | None = os.getenv("ANNOQ_DBSNP_RELEASE")
    ANNOQ_WGSA_VERSION:str | None = os.getenv("ANNOQ_WGSA_VERSION")
settings = Settings()
