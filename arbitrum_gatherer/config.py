import os

from dotenv import load_dotenv

load_dotenv()

NODE: str = os.getenv("NODE")
DATABASE: str = os.getenv("DATABASE")
DATABASE_CRED: str = os.getenv("DATABASE_CRED")
DATABASE_HOSTNAME: str = os.getenv("DATABASE_HOSTNAME")
