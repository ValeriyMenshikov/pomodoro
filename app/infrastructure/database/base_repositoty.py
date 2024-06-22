class BaseRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def execute(self, query, autocommit=True):
        async with self.db_session as session:
            result = await session.execute(query)
            if autocommit:
                await session.commit()
            return result
