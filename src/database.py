import asyncio
from typing import Annotated

from sqlalchemy import String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    # echo=True
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    ...