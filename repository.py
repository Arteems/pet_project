from sqlalchemy import select
import logging

from database import new_session, TaskOrm
from schemas import STaskAdd, STask


logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщений
)


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        try:
            async with new_session() as session:
                task_dict = data.model_dump()

                task = TaskOrm(**task_dict)
                session.add(task)
                await session.flush()
                await session.commit()
                return task.id
        except Exception as e:
            print(f"Возникла ошибка: {e}")
            return None

    @classmethod
    async def find_by_id(cls, task_id: int) -> TaskOrm | None:
        async with new_session() as session:
            task = await session.get(TaskOrm, task_id)
            return task

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            result = await session.execute(select(TaskOrm))
            task_models = result.scalars().all()

            logging.debug(f"Retrieved task models: {task_models}")

            # Преобразование объектов TaskOrm в словари
            task_schemas = [
                STask.model_validate(task_model.__dict__) for task_model in task_models
            ]

            logging.debug(f"Validated task schemas: {task_schemas}")

            return task_schemas

    @classmethod
    async def delete_one(cls, task_id: int) -> bool:
        async with new_session() as session:
            task = await session.get(TaskOrm, task_id)
            if task:
                await session.delete(task)
                await session.commit()
                return True
        return False

    @classmethod
    async def delete_all_tasks(cls) -> bool:
        try:
            async with new_session() as session:
                tasks = await session.execute(select(TaskOrm))
                tasks = tasks.scalars().all()
                if tasks:
                    for task in tasks:
                        await session.delete(task)
                    await session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Возникла ошибка: {e}")
            return False
