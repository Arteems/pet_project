from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router as tasks_router
from database_router import router as database_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logging.info("Выключение приложения")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(database_router)