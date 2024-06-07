import os
import certifi
from pydantic import BaseModel, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")


class Settings(BaseSettings):
    DEV:bool

    APP_NAME: str = "BOOK (LIBRARY) RECOMMENDATION SYSTEM"

    APPLICATION_CERTIFICATE: str = CERTIFICATE

    model_config = SettingsConfigDict(env_file=".env")


# Development-specific settings
class DevelopmentSettings(Settings):
    MONGODB_URL:str
    MONGODB_NAME: str = "Boilerplate"
    OPTION: str = "development_value"


# Production-specific settings
class ProductionSettings(Settings):
    MONGODB_URL: str
    OPTION: str = "production_value"


# Determine environment and choose appropriate settings
import dotenv

dotenv.load_dotenv()


if bool(os.getenv("DEV")) == True:
    settings = DevelopmentSettings()
else:
    settings = ProductionSettings()