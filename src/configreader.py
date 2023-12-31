import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class Config:
    bot_token: str = os.getenv("TOKEN")
    admin_id: str = os.getenv("ADMIN_ID")
    host: str = os.getenv("HOST")
    port: str = os.getenv("PORT")
    username: str = os.getenv("USERNAME")
    password: str = os.getenv("PASSWORD")


config = Config()
