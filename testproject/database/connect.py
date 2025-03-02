from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseConnection:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.session = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def close(self):
        await self.engine.dispose()
