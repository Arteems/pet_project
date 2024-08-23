from fastapi import APIRouter, HTTPException
from database import create_tables, delete_tables
import logging


router = APIRouter(prefix="/database", tags=["database"])


@router.post("/create_tables")
async def create_db_tables():
    try:
        await create_tables()
        logging.info("Таблица создана!")
        return {"message": "Таблица успешно создана"}
    except Exception as e:
        logging.error(f"Ошибка при создании таблицы: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании таблицы")


@router.delete("/create_tables")
async def delete_db_tables():
    try:
        await delete_tables()
        logging.info("Таблица удалена!")
        return {"message": "Таблица успешно удалена"}
    except Exception as e:
        logging.error(f"Ошибка удаления таблицы: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при удалении таблицы")
