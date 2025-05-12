import asyncpg
from dotenv import load_dotenv
import os
from database.config import get_db
from datetime import timedelta

load_dotenv()
async def save_message(user_id: int, message: str, response: str):
    conn = await get_db()
    await conn.execute(
        "INSERT INTO messages (user_id, message, response) VALUES ($1, $2, $3)",
        user_id, message, response
    )
    await conn.close()

async def clear_message_table():
    conn = await get_db()
    await conn.execute(
        "DELETE FROM messages"
    )
    await conn.close()

async def get_dialog():
    conn = await get_db()
    records = await conn.fetch(
        "SELECT user_id, message, response, created_at FROM messages"
    )
    await conn.close()
    return records

async def get_from_dishes(intent: str, column_name: str, value: str):
    conn = await get_db()
    records = await conn.fetch(
        f"SELECT {intent} FROM dishes WHERE {column_name} = $1",
        value
    )
    await conn.close()
    return records

async def get_names_through_time(value: timedelta, trait: str):
    conn = await get_db()
    records = await conn.fetch(
        f"SELECT name FROM dishes WHERE cooking_time {trait} $1",
        value
    )
    await conn.close()
    return records