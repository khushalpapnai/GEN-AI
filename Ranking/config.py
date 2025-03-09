import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_TTL_SECONDS = int(os.getenv("REDIS_TTL_SECONDS", "3600")) # 1 hour


    MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")


settings = Settings()