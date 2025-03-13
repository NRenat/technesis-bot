from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from models import UserExcelData
from config import config

engine = create_async_engine(config.BD_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def save_user_data_to_db(user_data: list[dict], user_id: int) -> None:
    async for session in get_async_session():
        user_data_objs = [
            UserExcelData(
                user=user_id,
                title=item['title'],
                url=str(item['url']),
                xpath=item['xpath'],
                price=item['price'],
            )
            for item in user_data
        ]
        try:
            session.add_all(user_data_objs)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
