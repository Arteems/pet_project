from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import logging

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Model(DeclarativeBase):
    pass


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    except Exception as e:
        logging.error(f"Ошибка создание таблицы: {e}")


async def delete_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
    except Exception as e:
        logging.error(f"Ошибка удаления таблицы: {e}")
