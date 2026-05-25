import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/bookdb")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "bookuser")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bookpass")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "bookdb")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

settings = Settings()