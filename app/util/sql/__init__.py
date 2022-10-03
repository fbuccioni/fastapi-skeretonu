from typing import Type, Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from ...sql import engine


__all__ = ('get_session', 'engine')


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def get_or_404(db: AsyncSession, model: Type[SQLModel], where: Any) -> SQLModel:
    instance: SQLModel = (
        await db.execute(
            select(model).where(where)
        )
    )\
        .first()

    if not instance:
        raise HTTPException(404)

    return instance


async def create(db, model: Type[BaseModel], sql_model: Type[SQLModel]):
    db_row = sql_model(**model.dict(skip_defaults=True))
    db.add(db_row)

    await db.commit()
    await db.update(db_row)

    return db_row


async def partial_update(
    db: AsyncSession, model: Type[BaseModel], sql_model: Type[SQLModel], where: Any
):
    db_row = (
        await db.execute(
            select(sql_model).where(where)
        )
    )\
        .first()

    if not db_row:
        raise HTTPException(404)

    for prop, value in model.dict(skip_defaults=True).items():
        setattr(db_row, prop, value)

    await db.add(db_row)
    await db.commit()
    await db.update(db_row)

    return db_row
