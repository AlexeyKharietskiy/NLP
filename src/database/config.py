import asyncpg
import logging
from dotenv import load_dotenv
import os

load_dotenv()

async def get_db():
    try:
        return await asyncpg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
    except Exception as e:
        logging.error(f"Ошибка подключения: {e}")
        raise