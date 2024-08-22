import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repository import TaskRepository
from schemas import STaskAdd, STask

router = APIRouter(prefix="/tasks", tags=["таски"])


@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()],
):
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("/{task_id}")
async def get_tasks_by_id(task_id: int) -> STask:
    task = await TaskRepository.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("")
async def get_all_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    logging.debug(f"Fetched tasks: {tasks}")
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    result = await TaskRepository.delete_one(task_id)
    return {"ok": result}
