import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.conf.config import config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session_scope(self):
        if self._session_maker is None:
            raise RuntimeError("Database session manager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise err
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session_scope() as session:
        yield session
