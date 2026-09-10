from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"  # .directory   filename

engine = create_async_engine(#connection to database
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

AyncSessionLocal = async_sessionmaker(
    engine,
    class_ = AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():#like open file
    async with AyncSessionLocal() as session:
        yield session


