from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router as tasks_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await delete_tables()
        logging.info("База очищена")
        await create_tables()
        logging.info("База готова к работе")
        yield
    except Exception as e:
        logging.error(f"Ошибка во время настройки базы данных: {e}")
    finally:
        logging.info("Выключение приложения")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
