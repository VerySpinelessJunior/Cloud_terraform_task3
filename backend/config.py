from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"  # HMAC-SHA256 algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = 30