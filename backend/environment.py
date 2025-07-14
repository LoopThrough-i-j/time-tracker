import os
from typing import Final


class EnvironmentVariables:
    # Mongo Configurations
    MONGO_HOST: Final[str] = os.getenv("MONGO_URL", str())
    MONGO_PASSWORD: Final[str] = os.getenv("MONGO_PASSWORD", str())
    MONGO_USERNAME: Final[str] = os.getenv("MONGO_USERNAME", str())
    MONGO_DATABASE: Final[str] = os.getenv("MONGO_DATABASE", str())
    MONGO_URI_FORMAT = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority"

    # App configs
    HOST: Final[str] = os.getenv("HOST", "0.0.0.0")
    PORT: Final[int] = int(os.getenv("PORT", 8080))
    ENV: Final[str] = os.getenv("APP_ENV", "DEV")
    DEBUG: Final[bool] = os.getenv("DEBUG") == "true"
    DOC_URL: Final[str | None] = os.getenv("DOC_URL", None)
    JWT_SECRET: Final[str] = os.getenv("JWT_SECRET", str())
