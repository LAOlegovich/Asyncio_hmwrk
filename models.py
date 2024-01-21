import os

from sqlalchemy import JSON, Column, Date, Integer, VARCHAR, String, Numeric, CheckConstraint
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "swapi")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRS_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRS_PORT}/{POSTGRES_DB}"


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"
    #id: Mapped[int] = mapped_column(primary_key=True)
    ID = Column(Integer, primary_key = True)
    birth_year = Column(VARCHAR(20), nullable = False)
    eye_color = Column(VARCHAR(20), nullable= False)
    films = Column(String)
    gender= Column(VARCHAR(20))
    hair_color =  Column(VARCHAR(20))
    height = Column(VARCHAR(20))
    homeworld = Column(VARCHAR(60))
    mass = Column(VARCHAR(20))
    name = Column(VARCHAR(40), nullable= False, unique = True)
    skin_color = Column(VARCHAR(20))
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)

    #__table_args__ = (
       # CheckConstraint(int(height) >= 1, name='check_height_positive'),
        #CheckConstraint(float(mass) > 0, name = 'check_mass_positive')
    #)
    #json: Mapped[dict] = mapped_column(JSON, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()
